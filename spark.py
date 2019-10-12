from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark import sql
from pyspark.sql import *
import pyspark
from pyspark.sql import functions as sf

from operator import add
import sys
## Constants
APP_NAME = "Spark_Job "
##OTHER FUNCTIONS/CLASSES

def main(sc,filename):
  full_df = spark.read.format("csv").option("header", "true").load(filename)
  
  data = full_df.select("id","brand","dateAdded","colors")
  print("data loaded succesfully")
  data.show(2)
  print("Starting to load data into redis")
  data.createOrReplaceTempView("data1")
  c = spark.sql("select a.id,a.brand,cast(a.dateAdded as date),a.colors from(select id,brand,dateAdded,colors,row_number() over(partition by cast(dateAdded as date) order by dateAdded) as rownum from data1) a where a.rownum = 1")
  c.write.format("org.apache.spark.sql.redis").option("table","getRecentItem").option("key.column","dateAdded").save()
  print("data loaded successfully")
  d = spark.sql("select brand,cast(dateAdded as date),count(brand) as count from data1 group by brand,cast(dateAdded as date) order by count(brand) desc ")
  print("Preparing to concat")
  d1 = d.withColumn('keys',sf.concat(sf.col('dateAdded'),sf.lit('_'),sf.col('brand')))
  print("concat done succesfully")
  d1 = d1.drop("dateAdded")
  d1.show(4)
  d1.write.format("org.apache.spark.sql.redis").option("table","getBrandsCount").option("key.column","keys").save()
  print("data loaded for brand count")
  e = spark.sql("select id,brand,cast(dateAdded as date),colors from data1 order by dateAdded desc")
  e = e.withColumn('keys',sf.concat(sf.col('colors'),sf.lit('_'),sf.col('dateAdded')))
  e.write.format("org.apache.spark.sql.redis").option("table","getItemsByColor").option("key.column","keys").save()
  print("data for the api's loaded successfully")

if __name__ == "__main__":

   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   spark = SparkSession(sc)
   sql_ctx = SQLContext(sc)
   filename = sys.argv[1]
   # Execute Main functionality
   main(sc, filename)
