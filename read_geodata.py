'''
The script connects and reads data from RLID gepspatial database

'''
import pyodbc
import pandas as pd

cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=rliddb.int.lcog.org,5433;"
                      "Database=RLIDGeo;"
                      "Trusted_Connection=yes;")

df = pd.read_sql_query('select * from dbo.BikeFacility', cnxn)
df.head()
list(df)
df.ftype.unique()
df.groupby(['ftype','ftypedes']).size().reset_index().rename(columns={0:'count'})
