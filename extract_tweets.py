import os
import re
import sys
import json

from pyspark.sql import *
import pyspark.sql.functions as F
from pyspark.sql.types import *
from datetime import datetime


def main(user, month, hashtag):
	spark = SparkSession.builder.getOrCreate()
	spark.conf.set('spark.sql.session.timeZone', 'UTC')
	sc = spark.sparkContext

	def contains(entry, x):
		return any(e.text == x for e in entry)


	contains_udf = F.udf(lambda entry: contains(entry, hashtag), BooleanType())

	df = spark.read.json('hdfs:///datasets/twitter_internetarchive/2017/'+month+'/*/*/*.json.bz2')
	df_cleaned = df.where((F.col('timestamp_ms').isNotNull()) & (F.col('entities').isNotNull()) & (F.col('entities.hashtags').isNotNull()))
	df_cleaned = df_cleaned.withColumn('timestamp_ms', df_cleaned.timestamp_ms.cast(LongType()))

	result = df_cleaned.filter(contains_udf(F.col('entities.hashtags')))
	result.write.mode('overwrite').parquet('sample_'+hashtag+'_'+month+'.parquet')

if __name__ == "__main__":
	if len(sys.argv) <= 3:
		print("No user name and month and hashtag provided")
	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
