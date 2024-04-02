# TechCo Data Preparation and Analysis

## Architecture Diagram

![Architecture Diagram](project_architecture.png)

## Requirements
- Resource Group
- Storage Account
- Key Vault
- Azure Databricks Workspace
- PySpark and SQL

## Execution
The code has been organized into notebooks. Each notebook can be executed individually and is independent from the other one. To execute the project, execute all the notebooks in order. 

## File Structure
Repo:
- 2ab. Transformation
    In this notebook, we mount the storage account and load all the files. To load the storage account, we used key vaults instead of hard-coding access keys. There were some minor inconsistencies, which were resolved after loading. 

- 2c. Join Tables
    In this notebook, all the tables were joined and stored to the same storage account. The joined tables are further used for exploratory data analysis and visualization.

- 3. Data Analysis and Viz.
    In this notebook, full data was loaded from the storage account and analyzed. This notebook also includes some graphs and plots.

- Readme.md

## Process Steps

### 1. Data Ingestion

The data is ingested from 3 sources(Customer details, product details, and activity logs) which are all flat-files:

1.1. customer_data.csv

This csv file contains details related to each customer of TechCo that has interacted with the TechCo Application. Currently, it stores basic details including customer_id, first_name, last_name,	email,	phone. The data for development has generated with the help of online sources which is then processed with custom scripts to transform it to a compatible format.

1.2. product_data.csv

This csv file contains details related to each product whose sale is hosted by TechCo. Currently, it stores basic details including a Product ID, the product name, category, and price. The data for development has generated with the help of a Python script (`Generate_Products.py`).

1.3. web_logs.json

This is a semi-structured JSON file that contains logs of all user activity on the TechCo website. Currently, it stores basic details including the ID of the customer performing a given action, the realted product's ID and quantity, the action performed, and the timestamp of the action(ignoring timezone) along with an ID for each log entry. For an entry where a certain value does not make much sense, the value for that field is kept as null instead of having a missing key. The data for development has generated with the help of a Python script (`web_logs.py`).

The data from all sources is ingested into Spark Dataframes in Python, for Transformation and other downstream activities.

### 2. Data Transformation

2.1. Casting IDs to match across Sources

2.2. Calculate total sales for each product

2.3. Create a Denormalized store having each log with the relevant customer's and product's details

### 3. Data Analysis and Visualization

3.1. Comparing the Frequency of actions performed

3.2. Finding the number of unique customers

3.3. Comparing revenues per product category

3.4. Finding the total sales across all activity

3.5. Comparing revenues per product

3.6. Comparing the total spend per customer
