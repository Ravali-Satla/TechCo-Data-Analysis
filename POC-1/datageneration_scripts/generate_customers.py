import pandas as pd


df = pd.read_csv('../../export.csv', index_col=False)

df = df.rename(columns={'id': 'customer_id'})

df['customer_id'] = df['customer_id'].apply(lambda x: 'CUST'+str(x))

df.to_csv('customer_data.csv', index=False)