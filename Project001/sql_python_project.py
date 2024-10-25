import kaggle

"""
!kaggle datasets download ankitbansal06/retail-orders -f orders.csv
# The above command is for the purpose of downloading the source dataset we would work on
"""
# To Extract the csv file from the downloaded zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip')
zip_ref.extractall()
zip_ref.close()

# Data Cleaning 
import pandas as pd
df = pd.read_csv('orders.csv')
df.head(20)

df=pd.read_csv('orders.csv',na_values=['Not Available','unknown'])
df['Ship Mode'].unique()

df.rename(columns={'Order Id':'order_id','City':'city'}) # or
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')

df['discount']=df['list_price']*df['discount_percent']*.01
df['sale_price']=df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")

df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)

# For SQL server connection, to export the data to server
import sqlalchemy as sal
engine = sal.create_engine(r'mssql://REVANTH\SQLEXPRESS/Python_sql_projects?driver=ODBC+DRIVER+17+FOR+SQL+SERVER')
conn=engine.connect()

"""
Note:
Before appending the data into server create the table with the same column name present in here
"""

df.to_sql('df_orders',con=conn,index=False,if_exists='append')
# By using the above command we've appended the data to sql server
