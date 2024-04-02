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

import pyspark.sql.functions as F
from pyspark.sql.types import IntegerType

web_logs_tmp = web_logs_df.withColumn('product_id', web_logs_df['product_id'].substr(-3,3).cast(IntegerType()))
web_logs_tmp.show()

# COMMAND ----------

products_table = product_df.createOrReplaceTempView('Products')
web_logs_table = web_logs_tmp.createOrReplaceTempView('Logs')
customer_table = customer_df.createOrReplaceTempView('Customer')

# COMMAND ----------

product_sales=spark.sql("SELECT (price*quantity) as sales, p.product_id, p.product_name FROM Products p inner join Logs L on p.product_id = L.product_id where action = 'purchase'")

# COMMAND ----------

display(product_sales)

# COMMAND ----------

sales_data_table = product_sales.createOrReplaceTempView('Product_sales')

# COMMAND ----------

# Comprehensive dataset for analysis
Ecom_data = spark.sql('SELECT L.log_id, L.timestamp, L.customer_id, L.product_id, L.action, L.quantity, p.product_name, p.category, p.price, c.first_name, c.last_name, c.email, c.phone FROM Products p join Logs L on p.product_id = L.product_id join Customer c  on L.customer_id = c.customer_id')

# COMMAND ----------

ecom_data_table = ecom_data.createOrReplaceTempView('Ecom_data')

# COMMAND ----------

display(Ecom_data)

# COMMAND ----------

# How many unique customers visited the website?
unique_customers = spark.sql('SELECT COUNT(DISTINCT customer_id) as unique_customers FROM Ecom_data WHERE action = "view" ')

display(unique_customers)

# COMMAND ----------

# Which product category generated the highest revenue?
top_category = spark.sql("SELECT a.category, SUM(b.sales) as revenue FROM Ecom_data a inner join Product_sales b on a.product_id = b.product_id GROUP BY category ORDER BY revenue DESC LIMIT 1")

display(top_category)



# COMMAND ----------

# Identify the top 10 customers based on their total spending
top_customers = spark.sql("SELECT a.customer_id, a.first_name, a.last_name, SUM(b.sales) as total_spending FROM Ecom_data a inner join Product_sales b on a.product_id = b.product_id GROUP BY customer_id, first_name, last_name ORDER BY total_spending DESC LIMIT 10")

display(top_customers)

# COMMAND ----------

import matplotlib.pyplot as plt
import pandas

# Convert PySpark DataFrame to Pandas DataFrame
pandas_unique_customers = unique_customers.toPandas()

# Get the unique customers count
unique_customers_count = pandas_unique_customers.iloc[0]['unique_customers']

# Create the bar plot using Matplotlib
plt.figure(figsize=(6, 4))
plt.bar(["Unique Customers"], [unique_customers_count])
plt.ylabel("Count")
plt.title("Number of Unique Customers Visited the Website")
plt.tight_layout()

# Display the plot
plt.show()


# COMMAND ----------

# Convert PySpark DataFrame to Pandas DataFrame
pandas_top_category = top_category.toPandas()

# Sort Pandas DataFrame by revenue
sorted_pandas_top_category = pandas_top_category.sort_values(by="revenue", ascending=False)

# Create the bar plot using Matplotlib
plt.figure(figsize=(6, 6))
plt.bar(sorted_pandas_top_category["category"], sorted_pandas_top_category["revenue"])
plt.xlabel("Product Category")
plt.ylabel("Revenue")
plt.title("Product Category Revenue")
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better visibility
plt.tight_layout()

# Display the plot
plt.show()


# COMMAND ----------

# Visualization 3: Top 10 Customers
# Convert PySpark DataFrame to Pandas DataFrame
pandas_top_customers = top_customers.toPandas()

# Sort Pandas DataFrame by total_spending
sorted_pandas_top_customers = pandas_top_customers.sort_values(by="total_spending", ascending=False)

# Create the bar plot using Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(sorted_pandas_top_customers["last_name"], sorted_pandas_top_customers["total_spending"])
plt.xlabel("Last Name")
plt.ylabel("Total Spending")
plt.title("Top 10 Customers by Total Spending")
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better visibility
plt.tight_layout()

# Display the plot
plt.show()
