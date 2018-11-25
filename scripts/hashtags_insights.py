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
	#df_cleaned = df_cleaned.withColumn('created_timestamp', F.to_timestamp('created_at', '%a %b %d %H:%M:%S +z %Y'))

	def create_entry(text, timestamp):
		return (text, Entry(1, timestamp, timestamp))

	def expand(entry):
		return [(x.text, entry.timestamp_ms) for x in entry.entities.hashtags]
		return [create_entry(x.text, entry.created_timestamp) for x in entry.entities.hashtags]

	def reduce_operation(a, b):
		return Entry(a.count + b.count, min(a.min_timestamp, b.min_timestamp), max(a.max_timestamp, b.max_timestamp))

	schema = StructType([
	    StructField("tag", StringType(), True),
	    StructField("timestamp", LongType(), True),
	])

	other = df_cleaned.rdd.flatMap(expand).toDF(schema)
	result = other.groupBy('tag').agg(F.count(F.lit(1)).alias('count'), F.min('timestamp').alias('min_timestamp'), F.max('timestamp').alias('max_timestamp'))
	result.write.mode('overwrite').parquet('hashtags'+month+'.parquet')
	"""
	counts = df_cleaned.rdd.flatMap(expand).reduceByKey(reduce_operation).collect()
	print(counts)
	print(type(counts))
	f = open("counts_hashtags.json", "w")
	f.write(json.dumps(dict(counts)))
	f.close()
	df_cleaned.show(10)
	"""
if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print("No user name and month provided")
	else:
		main(sys.argv[1], sys.argv[2])
