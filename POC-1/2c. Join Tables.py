# Databricks notebook source
storage_account = 'saprojectgroup'
container_name = 'data'
source_url = f'wasbs://{container_name}@{storage_account}.blob.core.windows.net'

# COMMAND ----------

mount_name = "sa"
mount_point_url = f'/mnt/{mount_name}'

extra_configs_key = f'fs.azure.account.key.{storage_account}.blob.core.windows.net'
extra_configs_value = access_key
extra_configs_dict = {extra_configs_key:extra_configs_value}

# COMMAND ----------

dbutils.fs.mount(source = source_url,
                 mount_point = mount_point_url,
                 extra_configs = {
                     extra_configs_key: extra_configs_value
                 })


# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder.appName("TechCoECommerce").getOrCreate()

# COMMAND ----------

# Load web logs data
web_logs_df = spark.read.option("multiline","true").json(f"/mnt/{mount_name}/web_logs.json")

# Load customer data
customer_df = spark.read.csv(f"/mnt/{mount_name}/customer_data.csv", header=True, inferSchema=True)

# Load product data
product_df = spark.read.csv(f"/mnt/{mount_name}/product_data.csv", header=True, inferSchema=True)

# COMMAND ----------

display(customer_df)

# COMMAND ----------

display(product_df)

# COMMAND ----------

display(web_logs_df)

# COMMAND ----------

product_df.count()

# COMMAND ----------

from pyspark.sql.types import IntegerType

web_logs_tmp = web_logs_df.withColumn('product_id', web_logs_df['product_id'].substr(-3,3).cast(IntegerType()))

web_logs_tmp.show()

# type(product_df.product_id)

# COMMAND ----------

# Question 
# customer_df.join(product_df.join(web_logs_tmp,product_df.product_id == web_logs_df.product_id,"inner"),customer_df.customer_id 
# == customer_df.customer_id,"inner").show()

# (product_df.product_id == web_logs_tmp.product_id).show()

product_df.join(web_logs_tmp,product_df.product_id == web_logs_tmp.product_id,"inner")
