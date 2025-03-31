import os
from pyspark.sql import SparkSession, DataFrame
from abc import abstractmethod


class DataProcessor:
    def __init__(self):
        self._spark = SparkSession.builder.master("local[*]").appName('Spark Session').getOrCreate()
        self._working_folder = self._set_working_folder()
        self._destiny_folder = self._set_destiny_folder()

    def _write_csv(self, folder_name: str, spark_df: DataFrame):
        output_path = f"{self._destiny_folder}{folder_name}"
        print(output_path)
        (
            spark_df.write
            .format("csv")
            .option("header", "true")
            .mode("overwrite")
            .save(f"{output_path}")  # "file:///" is required
        )

    @abstractmethod
    def _set_working_folder(self):
        pass

    @abstractmethod
    def _set_destiny_folder(self):
        pass

    @abstractmethod
    def _process(self):
        pass
