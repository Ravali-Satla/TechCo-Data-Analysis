# Databricks notebook source
# Imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# COMMAND ----------

# Load the transformed data from Storage account
storage_account = 'saprojectgroup'
container_name = 'data'
source_url = f'wasbs://{container_name}@{storage_account}.blob.core.windows.net'

access_key = dbutils.secrets.get(
    scope= "storage-account",
    key= "sa-key"
)
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

df = spark.read.csv(f"/mnt/{mount_name}/full_data.csv", header=True, inferSchema=True)
display(df)

# COMMAND ----------

tmp_df = df.toPandas()
ax = tmp_df['action'].hist(bins=3, grid=False, figsize=(12,8), color='#86bf91', width=0.6)

ax.set_xlabel('Action')
ax.set_ylabel('Count')
ax.set_title('Distribution by Action')


# COMMAND ----------

# How many unique customers visited the website?
n_views = df.filter(df.action == 'view')
n_views_distinct = n_views.dropDuplicates(['customer_id']).select('customer_id')
print("The number of distinct customers: ", n_views_distinct.count())

# COMMAND ----------

# Which product category generated the highest revenue?
purchased_products = df.filter(df.action == 'purchase')
purchased_products.show(5)

# COMMAND ----------

total_amount = purchased_products.withColumn('amount', df.quantity * df.price)
total_amount.show(5)

# COMMAND ----------

revenue = total_amount.groupBy('product_id').sum('amount').withColumnRenamed('sum(amount)', 'total_sale').sort('product_id')
revenue.show()

# COMMAND ----------

revenue_pd = revenue.toPandas()
ax = revenue_pd.plot.bar(x='product_id', y='total_sale', figsize=(10,16), color='#86bf91')
ax.set_xlabel('Product Id')
ax.set_ylabel('Sales')
ax.set_title('Sales by Product')

# COMMAND ----------

max_revenue = revenue.sort(revenue.total_sale.desc())

max_revenue.show(1)

# COMMAND ----------

print(f'The product {max_revenue.collect()[0][0]} brought the most revenue {max_revenue.collect()[0][1]}')


# COMMAND ----------

# Identify the top 10 customers based on their total spending

customer_group = total_amount.groupBy('customer_id').sum('amount').withColumnRenamed('sum(amount)', 'total_purchase')
customer_group.show(5)

# COMMAND ----------

top_10_customer = customer_group.sort(customer_group.total_purchase.desc())
print("The Top 10 customers with highest spending are: ")
top_10_customer.show(10)

# COMMAND ----------

customer_pd = top_10_customer.limit(10).toPandas()
ax = customer_pd.plot.bar(x='customer_id', y='total_purchase', figsize=(10,16), color='#86bf91')
ax.set_xlabel('Customer Id')
ax.set_ylabel('Purchase')
ax.set_title('Purchases by Customers')
