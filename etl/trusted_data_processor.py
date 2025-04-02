import pyspark.sql.functions as F
from data_processor import DataProcessor
from pyspark.sql.functions import *
from pyspark.sql.window import Window


class TrustedDataProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.__products_df, self.__sites_df, self.__sales_df, self.__stock_df = self.__get_data_local()
        self._process()

    @staticmethod
    def _set_working_folder():
        return '../trusted_data/'

    @staticmethod
    def _set_destiny_folder():
        return '../refined_data/'

    def __get_data_local(self):
        files = ['products', 'sites', 'sales', 'stock']
        data = []
        for file in files:
            data.append(self._spark.read.csv(path=f'{self._working_folder}{file}', sep=',', header=True))

        return data

    def __join_with_products_and_sites(self, df: DataFrame, column_name: str) -> DataFrame:
        enriched_df = df.join(self.__products_df, on='sku', how='left')
        enriched_df = enriched_df.join(self.__sites_df, on='site_code', how='left')
        enriched_df = enriched_df.withColumnRenamed('brand_name', 'product_name')
        enriched_df = enriched_df.withColumn(column_name,
                                             (col('quantity') * col('units_per_package')).cast('integer'))
        enriched_df = enriched_df.drop('full_date', 'country_code')
        return enriched_df

    def __generate_enriched_sales(self) -> DataFrame:
        enriched_sales_df = self.__join_with_products_and_sites(self.__sales_df, 'units_sold')
        enriched_sales_df = enriched_sales_df.withColumnRenamed('quantity', 'items_sold')
        return enriched_sales_df

    def __generate_enriched_stock(self) -> DataFrame:
        enriched_stock_df = self.__join_with_products_and_sites(self.__stock_df, 'units_in_stock')
        enriched_stock_df = enriched_stock_df.withColumnRenamed('quantity', 'items_in_stock')
        return enriched_stock_df

    def __generate_insights(self, enriched_sales_df: DataFrame, enriched_stock_df: DataFrame):
        # ======== historical sales per month =================
        sales_per_month = (enriched_sales_df.groupBy('month', 'year', 'product_name').agg(
            sum('items_sold').cast('integer').alias('items_sold')))
        self._write_csv('summary_sales_month', sales_per_month)
        # ======== historical sales per week day =================
        sales_per_weekday = (enriched_sales_df.groupBy('weekday_name', 'month', 'year', 'product_name').agg(
            sum('items_sold').cast('integer').alias('items_sold')))
        self._write_csv('summary_sales_per_weekday', sales_per_weekday)
        # ======== popularity score per month =================
        percentiles = (
            enriched_sales_df.groupBy("month", "year", "product_name")
            .agg(F.sum("units_sold").cast("integer").alias("total_units_sold"))
            .groupBy("month", "year")
            .agg(
                expr("percentile_approx(total_units_sold, 0.25)").alias("p25"),
                expr("percentile_approx(total_units_sold, 0.50)").alias("p50"),
                expr("percentile_approx(total_units_sold, 0.75)").alias("p75"),
                F.min("total_units_sold").alias("min_sold"),
                F.max("total_units_sold").alias("max_sold")
            )
        )
        monthly_popularity_score = (
            enriched_sales_df.groupBy("month", "year", "product_name")
            .agg(F.sum("units_sold").cast("integer").alias("total_units_sold"))
            .join(percentiles, ["month", "year"])
            .withColumn("popularity_score",
                        when(col("total_units_sold") >= col("p75"), lit(80) + (lit(20) * (col("total_units_sold") - col("p75")) / (col("max_sold") - col("p75"))))
                        .when(col("total_units_sold") >= col("p50"), lit(50) + (lit(30) * (col("total_units_sold") - col("p50")) / (col("p75") - col("p50"))))
                        .when(col("total_units_sold") >= col("p25"), lit(20) + (lit(30) * (col("total_units_sold") - col("p25")) / (col("p50") - col("p25"))))
                .otherwise((lit(20) * (col("total_units_sold") - col("min_sold"))) / (col("p25") - col("min_sold")))
            )
            .withColumn("popularity_score", least(greatest(col("popularity_score"), lit(0)), lit(100)))
        )
        monthly_popularity_score = monthly_popularity_score.drop('p25', 'p50', 'p75')
        self._write_csv('monthly_popularity_score', monthly_popularity_score)

        # ======================Special Days=================================
        daily_sales = enriched_sales_df.groupBy("year", "month", "day").agg(
            sum("items_sold").cast('integer').alias("daily_sales"))
        monthly_stats = (daily_sales.groupBy("year", "month").agg(
            expr("percentile_approx(daily_sales, 0.25)").alias("q1"),
            expr("percentile_approx(daily_sales, 0.75)").alias("q3")))

        daily_with_iqr = daily_sales.join(monthly_stats, ["year", "month"]) \
            .withColumn("iqr", F.col("q3") - F.col("q1")) \
            .withColumn("monthly_lower_bound", F.col("q1") - 1.5 * F.col("iqr")) \
            .withColumn("monthly_upper_bound", F.col("q3") + 1.5 * F.col("iqr"))

        special_days_for_sales = daily_with_iqr.filter(
            (col("daily_sales") < col("monthly_lower_bound")) | (col("daily_sales") > col("monthly_upper_bound")))
        special_days_for_sales = special_days_for_sales.drop('q1', 'q3', 'iqr')
        self._write_csv('special_days_for_sales', special_days_for_sales)

        # ======================Stock Analysis=================================
        no_stock_days = enriched_stock_df.filter(col('items_in_stock') == 0)
        no_stock_days = no_stock_days.groupBy('product_name', 'country_name').count().alias('no_stock_days')
        self._write_csv('summary_no_stock_days', no_stock_days)

    def _process(self):
        enriched_sales_df = self.__generate_enriched_sales()
        enriched_stock_df = self.__generate_enriched_stock()
        self.__generate_insights(enriched_sales_df, enriched_stock_df)
        # full_sales and full_stock are tables that will use LLM for predictions and data queries
        full_sales = enriched_sales_df.drop('units_sold', 'zip_code', 'barcode', 'package_type')
        self._write_csv('sales', full_sales)
        full_stock = enriched_stock_df.drop('barcode', 'package_type', 'units_in_stock', 'zip_code')
        self._write_csv('stock', full_stock)
