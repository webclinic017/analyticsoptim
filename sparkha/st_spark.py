from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, DataFrameReader

import pandas as pd

logFile = "file:///home/lohrasp/programs/spark/README.md"
# sc = SparkContext("local", "first app")
# logData = sc.textFile(logFile).cache()
# numAs = logData.filter(lambda s: 'a' in s).count()
# numBs = logData.filter(lambda s: 'b' in s).count()
# print ("Lines with a: %i, lines with b: %i" % (numAs, numBs))
spark = SparkSession.builder.getOrCreate()
# df = spark.read.json("/home/lohrasp/programs/spark/examples/src/main/resources/people.json")
#
# print(df)
# df = pd.read_html("localhost:4040/executors")[1]
# print(df)
# from pyspark.sql import SparkSession
#
# spark = SparkSession \
#     .builder \
#     .appName("Python Spark K-means example") \
#     .config("spark.some.config.option", "some-value") \
#     .getOrCreate()
#
# df = spark.read.format('com.databricks.spark.csv'). \
#     options(header='true',
#             inferschema='true'). \
#     load("iris.csv", header=True)
# df.show(5,True)

# from pyspark import SparkContext
# sc = SparkContext("local", "First App")
# RDDread = sc.textFile(logFile).cache()
# print(RDDread.take(7))
# print(RDDread.takeSample(False,10,4))
# # spark = SparkSession.builder.getOrCreate()


import os
sparkClassPath = os.getenv('SPARK_CLASSPATH', '/home/lohrasp/programs/spark/jars/postgresql-42.2.14.jar')
jar_path = "/home/lohrasp/programs/spark/jars/postgresql-42.2.14.jar"
# print("jar exists:", os.path.isfile(jar_path))

os.environ['PYSPARK_SUBMIT_ARGS'] = f'--jars {jar_path} pyspark-shell'
conf = SparkConf()
conf.setAppName('postgres test')
conf.set('spark.jars', 'file:%s' % sparkClassPath)
conf.set('spark.executor.extraClassPath', sparkClassPath)
conf.set('spark.driver.extraClassPath', sparkClassPath)

url = 'postgresql://192.168.0.108:5432/testdb1'
properties = {'user':'postgres', 'password':'reallyStrongPwd123'}

df = DataFrameReader(spark).jdbc(url='jdbc:%s' % url, table='tablename', properties=properties)


# from pyspark.sql import SparkSession
#
# url = "jdbc:postgresql://192.168.0.108:5432/testdb1"
# properties = {
#     "user": "postgres",
#     "password": "reallyStrongPwd123"
# }
#
# spark = SparkSession.builder.master("local") \
#     .appName("Python Spark SQL basic example") \
#     .config("spark.jars", jar_path) \
#     .getOrCreate()
#
# df = spark.read.format("jdbc").option("url", url) \
#     .option("dbtable", "stocks").option("password", "reallyStrongPwd123")\
#     .option("user", "postgres").option("driver", "org.postgresql.Driver").load()

# df = spark.read \
#     .format("jdbc") \
#     .option("url", url) \
#     .option("dbtable", "stocks") \
#     .option("user", "postgres") \
#     .option("password", "reallyStrongPwd123") \
#     .option("driver", "org.postgresql.Driver") \
#     .load()
# df.printSchema()

# from pyspark.sql import DataFrameReader
#
# url = 'postgresql://192.168.0.108:5432/testdb1'
# properties = {'user': 'postgres', 'password': 'reallyStrongPwd123', 'driver': 'org.postgresql.Driver'}
# df = DataFrameReader(spark).jdbc(
#     url="jdbc:{ url}, table='weather', properties=properties
# )
# df.show()
