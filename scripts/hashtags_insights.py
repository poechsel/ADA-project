import os
import re
import sys
import json

from pyspark.sql import *
import pyspark.sql.functions as F
from pyspark.sql.types import *
from datetime import datetime


class Entry:
	def __init__(self, c, min_t, max_t):
		self.count = c
		self.min_timestamp = min_t
		self.max_timestamp = max_t

def main(user, month):
	spark = SparkSession.builder.getOrCreate()
	spark.conf.set('spark.sql.session.timeZone', 'UTC')
	sc = spark.sparkContext


	df = spark.read.json('hdfs:///datasets/twitter_internetarchive/2017/'+month+'/*/*/*.json.bz2')


	df_cleaned = df.where((F.col('timestamp_ms').isNotNull()) & (F.col('entities').isNotNull()) & (F.col('entities.hashtags').isNotNull()))
	df_cleaned = df_cleaned.withColumn('timestamp_ms', df_cleaned.timestamp_ms.cast(LongType()))
	df_cleaned = df_cleaned.withColumn('timestamp', F.from_unixtime(F.col('timestamp_ms')/1000).cast(DateType()))
	df_cleaned = df_cleaned.withColumn('day_tweet', F.dayofmonth(F.col('timestamp')))
	def expand(entry):
	    return [(x.text, entry.day_tweet, entry.user.followers_count) for x in entry.entities.hashtags]

	schema = StructType([
	    StructField("tag", StringType(), True),
	    StructField("day", LongType(), True),
	    StructField("follower_count", LongType(), True),
	])
	days = range(1, 31 + 1)
	exprs_days = [F.sum((F.col('day')==day).cast("long")).alias('count_'+str(day)) for day in days]
	exprs_print = [F.sum((F.col('day')==day).cast("long") * F.col('follower_count')).alias('print_'+str(day)) for day in days]
	other = df_cleaned.rdd.flatMap(expand).toDF(schema)
	result = other.groupBy('tag').agg(F.count(F.lit(1)).alias('count'), F.sum(F.col('follower_count')).alias('print'), *(exprs_print + exprs_days))

	result.write.mode('overwrite').parquet('hashtags_insights_'+month+'.parquet')

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print("No user name and month provided")
	else:
		main(sys.argv[1], sys.argv[2])
