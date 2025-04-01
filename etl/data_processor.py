import os
from pyspark.sql import SparkSession, DataFrame
from abc import abstractmethod


class DataProcessor:
    def __init__(self):
        #---------------- S3 - implementation -------------- Start
        # self.__spark = (SparkSession.builder.appName("CodeRoadFinalProject")
        #                 .config("spark.hadoop.fs.s3a.access.key", "")  # Leave empty to use ~/.aws/credentials
        #                 .config("spark.hadoop.fs.s3a.secret.key", "")  # Leave empty to use ~/.aws/credentials
        #                 .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
        #                 .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        #                 .getOrCreate())
        # self.__s3_path = 's3a://coderoad-final-project/'
        # ---------------- S3 - implementation -------------- End

        self._spark = SparkSession.builder.master("local[*]").appName('CodeRoadFinalProject').getOrCreate()
        self._working_folder = self._set_working_folder()
        self._destiny_folder = self._set_destiny_folder()

    def _write_csv(self, folder_name: str, spark_df: DataFrame):
        output_path = f"{self._destiny_folder}{folder_name}"
        (
            spark_df.write
            .format("csv")
            .option("header", "true")
            .mode("overwrite")
            .save(f"{output_path}")
        )

    @staticmethod
    @abstractmethod
    def _set_working_folder():
        pass

    @staticmethod
    @abstractmethod
    def _set_destiny_folder():
        pass

    @abstractmethod
    def _process(self):
        pass
