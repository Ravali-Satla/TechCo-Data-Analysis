# Databricks notebook source
ACCESS_KEY = dbutils.secrets.get(scope = "aws", key = "aws-access-key")
SECRET_KEY = dbutils.secrets.get(scope = "aws", key = "aws-secret-access-key")
ENCODED_SECRET_KEY = SECRET_KEY.replace("/", "%2F")
AWS_BUCKET_NAME = "bkt-poc2-training"
MOUNT_NAME = "bkt-mount"

dbutils.fs.mount("s3a://%s:%s@%s" % (ACCESS_KEY, ENCODED_SECRET_KEY, AWS_BUCKET_NAME), "/mnt/%s" % MOUNT_NAME)
display(dbutils.fs.ls("/mnt/%s" % MOUNT_NAME))

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder.appName("S3connectiontest").getOrCreate()

# COMMAND ----------

customer_df = spark.read.csv(f"/mnt/{MOUNT_NAME}/input/customer_data.csv",header=True)

display(customer_df)

# COMMAND ----------


