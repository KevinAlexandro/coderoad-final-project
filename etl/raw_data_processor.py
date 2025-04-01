import pycountry
from pyspark.sql.functions import *
from data_processor import DataProcessor
from pyspark.sql import DataFrame


class RawDataProcessor(DataProcessor):

    def __init__(self):
        super().__init__()
        self.__products_df, self.__sites_df, self.__sales_df, self.__stock_df = self.__get_data_local()
        self._process()

    @staticmethod
    def _set_working_folder():
        return '../raw_data/'

    @staticmethod
    def _set_destiny_folder():
        return '../trusted_data/'

    def get_country_df(self):
        country_tuples = [(c.alpha_2, c.name) for c in pycountry.countries]
        return self._spark.createDataFrame(country_tuples, ['country_code', 'country_name'])

    @staticmethod
    def __transform_date(df: DataFrame):
        trusted_date_df = (df
                           .withColumn('year', year(col('date')))
                           .withColumn('month', month(col('date')))
                           .withColumn('day', day(col('date')))
                           .withColumn('weekday_name', date_format(col('date'), 'EEEE'))
                           )
        trusted_date_df = trusted_date_df.withColumnRenamed('date', 'full_date')
        return trusted_date_df

    def __get_data_local(self):
        files = ['products', 'sites', 'sales', 'stock']
        data = []
        for file in files:
            data.append(self._spark.read.csv(path=f'{self._working_folder}{file}.csv', sep=',', header=True))

        return data

    def __transform_products(self):
        trusted_products = self.__products_df.withColumn(
            'units_per_package',
            when(lower(col('package_type')) == 'single', 1)
            .otherwise(regexp_extract(col('package_type'), r'^(\d+)', 1).cast('int'))
        )
        self._write_csv('products', trusted_products)

    def __transform_sites(self):
        # Join with main DataFrame
        trusted_sites = self.__sites_df.withColumnRenamed('country', 'country_code')
        trusted_sites = trusted_sites.join(self.get_country_df(), how='left', on='country_code')
        self._write_csv('sites', trusted_sites)

    def __transform_sales(self):
        trusted_sales = self.__transform_date(self.__sales_df)
        self._write_csv('sales', trusted_sales)

    def __transform_stock(self):
        trusted_stock = self.__transform_date(self.__stock_df)
        trusted_stock = trusted_stock.withColumnRenamed('stock', 'quantity')
        self._write_csv('stock', trusted_stock)

    def _process(self):
        self.__transform_products()
        self.__transform_sites()
        self.__transform_sales()
        self.__transform_stock()
