# Scripts

This folder contains different scripts used to extract insights and data from the twitter dataset.

## Usage:

To use a script `script.py` on the cluster, type the following command:

```
ssh USERNAME@iccluster028.iccluster.epfl.ch "nohup spark-submit --master yarn --deploy-mode client --driver-memory 4G --num-executors 5 --executor-memory 4G --executor-cores 5 script.py arg1 ... argn"
```


## extract_tweets.py

This script will extract every tweets made on a given month and containing a given hashtag.

### Usage:

```
extract_tweets.py username month hashtag
```

Where:
- `username` is your EPFL username.
- `month` is a two digit string corresponding to a month (01, 02, ..., 10, 11, ...)
- `hashtag` is an hashtag

A parquet file named `sample_[hashtag]_[month].parquet` will be created on spark.


## hashtags_insight.py

This script will, given a month, create a dataframe representing 'insights' for an hashtags. Currently it is a database containing one row by hashtag occuring during the month given as argument. Each row have the following information:

- `tag`: text of the hashtag
- `count`: number of occurences of this hashtag
- `min_timestamp`: first date (in millisecond) at which the hashtag appeared during the month
- `max_timestamp`: last date (in millisecond) at which the hashtag appeared during the month



### Usage:

```
hashtags_insight.py username month
```

Where:
- `username` is your EPFL username.
- `month` is a two digit string corresponding to a month (01, 02, ..., 10, 11, ...)

A parquet file named `hashtags_[month].parquet` will be created on spark.
