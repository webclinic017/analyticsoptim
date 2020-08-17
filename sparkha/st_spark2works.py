from pyspark import SparkContext, SparkConf
from pyspark.sql import DataFrameReader, SQLContext
import os

sparkClassPath = os.getenv('SPARK_CLASSPATH', '/home/lohrasp/programs/spark/jars/postgresql-42.2.14.jar')

# Populate configuration
conf = SparkConf()
conf.setAppName('application')
conf.set('spark.jars', 'file:%s' % sparkClassPath)
conf.set('spark.executor.extraClassPath', sparkClassPath)
conf.set('spark.driver.extraClassPath', sparkClassPath)
# Uncomment line below and modify ip address if you need to use cluster on different IP address
# conf.set('spark.master', 'spark://127.0.0.1:7077')

sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

url = 'postgresql://slave:5432/testdb1'
properties = {'user':'postgres', 'password':'reallyStrongPwd123'}

df = DataFrameReader(sqlContext).jdbc(url='jdbc:%s' % url, table='stocks', properties=properties)

df.printSchema()
df.show()