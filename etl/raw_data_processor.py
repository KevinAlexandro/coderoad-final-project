from os.path import split
from pyspark.sql.functions import *
from data_processor import DataProcessor
from enum import Enum

# Ranges from 1 for a Sunday through to 7 for a Saturday
DAYS = {
    1: "Sunday",
    2: "Monday",
    3: "Tuesday",
    4: "Wednesday",
    5: "Thursday",
    6: "Friday",
    7: "Saturday"
}

class RawDataProcessor(DataProcessor):

    def __init__(self):
        super().__init__()
        self.__products, self.__sites, self.__sales, self.__stock = self.__get_data_local()
        self._process()

    def _set_working_folder(self):
        return '../raw_data/'

    def _set_destiny_folder(self):
        return '../trusted_data/'

    def __get_data_local(self):
        files = ['products', 'sites', 'sales', 'stock']
        data = []

        for file in files:
            data.append(self._spark.read.csv(path=f'{self._working_folder}{file}.csv', sep=',', header=True))

        return data

    def __transform_products(self):
        # no need to change anything in products
        self._write_csv('products', self.__products)

    def __transform_sites(self):
        # no need to change anything in sites
        self._write_csv('sites', self.__sites)

    def __transform_sales(self):
        # trusted_sales = self.__sales.withColumn('year', year(col('date')))
        # trusted_sales = trusted_sales.withColumn('month', month(col('date')))
        # trusted_sales = trusted_sales.withColumn('day', day(col('date')))
        #
        # trusted_sales = trusted_sales.withColumn('day_of_week', create_map([lit(x) for x in DAYS.items()])[col('day_of_week_num')])
        trusted_sales = (self.__sales
                         .withColumn('year', year(col('date')))
                         .withColumn('month', month(col('date')))
                         .withColumn('day', day(col('date')))
                         .withColumn('day_of_week', create_map([lit(x) for x in DAYS.items()])[col('day_of_week_num')])
                         )
        trusted_sales.show()

    def __transform_stock(self):
        pass

    def _process(self):
        self.__transform_products()
        self.__transform_sites()
        self.__transform_sales()
        self.__transform_stock()
