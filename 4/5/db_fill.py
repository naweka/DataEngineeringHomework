import sqlite3
import pandas as pd

conn = sqlite3.connect('db.db')


products_df = pd.read_csv('products.csv')
customers_df = pd.read_csv('customers.csv')
purchases_df = pd.read_csv('purchases.csv')


products_df.to_sql('products', conn, if_exists='append', index=False)
customers_df.to_sql('customers', conn, if_exists='append', index=False)
purchases_df.to_sql('purchases', conn, if_exists='append', index=False)