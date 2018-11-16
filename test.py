import os
import re
import sys

from pyspark.sql import *
from pyspark.sql.functions import unix_timestamp, udf, to_date
from pyspark.sql.types import ArrayType, StringType, IntegerType
from datetime import datetime

def main(user):
	spark = SparkSession.builder.getOrCreate()
	spark.conf.set('spark.sql.session.timeZone', 'UTC')
	sc = spark.sparkContext


	df = spark.read.json('hdfs:///datasets/twitter_internetarchive/*/*/*/*/*.json.bz2')
	#print(df.count())
	df.printSchema()


	v = df._jdf.schema().treeString()
	sc.parallelize([v]).saveAsTextFile("hdfs:///user/{}/schema.txt".format(user))

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print("No user name provided")
	else:
		main(sys.argv[1])
