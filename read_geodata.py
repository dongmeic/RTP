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

import geopandas as gpd
from sqlalchemy import create_engine

engine = create_engine(   
"mssql+pyodbc:///?odbc_connect="
"Driver%3D%7BODBC+Driver+17+for+SQL+Server%7D%3B"
"Server%3Drliddb.int.lcog.org%2C5433%3B"
"Database%3DRLIDGeo%3B"
"Trusted_Connection%3Dyes%3B"
"ApplicationIntent%3DReadWrite%3B"
"WSID%3Dclwrk4087.int.lcog.org%3B")

sql = '''
SELECT CAST(bike_segid as varchar) AS id, ftype, ftypedes, Shape.STAsBinary() AS geom
FROM dbo.BikeFacility;
'''

BikeFacility = gpd.GeoDataFrame.from_postgis(sql, engine, geom_col='geom' )

import matplotlib.pyplot as plt
import contextily as ctx

MPObd = gpd.read_file("V:/Data/Transportation/MPO_Boundary.shp")
BikeFacility.crs = "EPSG:4152"

fig, ax = plt.subplots(figsize=(14, 12))
BikeFacility.plot(ax=ax, column='ftype', cmap='Set1', legend=True, aspect=1)
MPObd.plot(ax=ax, facecolor="none", edgecolor="black", linestyle='--', aspect=1)
ctx.add_basemap(ax)
plt.title("Bike Facilities in Lane County", fontsize=30, fontname="Palatino Linotype", color="grey")
ax.axis("off")
plt.show()