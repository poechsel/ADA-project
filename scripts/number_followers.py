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


	df_cleaned = df.where((F.col('user').isNotNull()))
	df_cleaned = df.where((F.col('user.id').isNotNull()) & (F.col('user.followers_count').isNotNull())) 
	df_cleaned = df_cleaned.withColumn('userId', df_cleaned.user.id)
	df_cleaned = df_cleaned.withColumn('followersCount', df_cleaned.user.followers_count)
	df_cleaned = df_cleaned.select('userId', 'followersCount')

	result = df_cleaned

	result.write.mode('overwrite').parquet('followers_count_'+month+'.parquet')

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		print("No user name and month provided")
	else:
		main(sys.argv[1], sys.argv[2])
