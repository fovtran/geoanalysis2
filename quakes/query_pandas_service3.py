# diego
import pandas as pd
pd.set_option('display.max_rows', 1000)
from numpy import array, ones, ma, meshgrid, where, exp

# accelerogramas la palma
# https://www.ign.es/web/ign/portal/sis-catalogo-acelerogramas/-/catalogo-acelerogramas/searchAcelerograma?latMin=28.212&latMax=28.984&longMin=-18.237&longMax=-17.364&startDate=01/01/2010&endDate=31/10/2021&selIntensidad=N&selMagnitud=N&intMin=&intMax=&magMin=&magMax=&selProf=N&profMin=&profMax=&cond=
# Sismos region palma
# https://www.ign.es/web/ign/portal/sis-catalogo-terremotos/-/catalogo-terremotos/searchTerremoto?latMin=26.6412193530742&latMax=30.244734978074202&longMin=-19.694437169627594&longMax=-15.212015294627593&startDate=01/01/2010&endDate=25/10/2021&selIntensidad=N&selMagnitud=N&intMin=&intMax=&magMin=&magMax=&selProf=N&profMin=&profMax=&fases=no&cond=
filename = 'catalogoComunSV_1635195668083.csv'
df = pd.read_csv(filename, delimiter=';', skipinitialspace = True) #, parse_dates=[['Fecha', 'Hora']])

for key in df.keys():
    newcolumnname = key.replace(' ', '').replace('.','')
    df = df.rename(columns={key: newcolumnname})

df = df.rename(columns={'Evento': 'i'})
df.set_index('i', inplace=True)

df.drop('TipoMag', axis=1, inplace=True)
df.drop('Inten', axis=1, inplace=True)

df["DateTime"] = df["Fecha"] + ' ' + df["Hora"]
df[["DateTime"]] = df[["DateTime"]].apply(pd.to_datetime)
df.drop('Hora', axis=1, inplace=True)
df.drop('Fecha', axis=1, inplace=True)
df.drop('Localización', axis=1, inplace=True)

# Bounding box
maxlat=28.984
minlon=-18.237
maxlon=-17.364
minlat=28.212
df = df.drop(df[df.Latitud <minlat].index)
df = df.drop(df[df.Latitud >maxlat].index)
df = df.drop(df[df.Longitud <minlon].index)
df = df.drop(df[df.Longitud >maxlon].index)

start_date = "2021-09-1"
end_date = "2021-10-25"

after_start_date = df["DateTime"] >= pd.to_datetime(start_date,infer_datetime_format=True)
before_end_date = df["DateTime"] <= pd.to_datetime(end_date,infer_datetime_format=True)
between_two_dates = after_start_date & before_end_date
df = df.loc[between_two_dates]

#df = df[df.Mag >2.5].sort_values(['Localización', 'Mag', 'Prof(Km)'])
print(df)

d = df.describe(percentiles=[.05,.10,.20,.25,.30,.40,.45,.50,.60,.70,.75,.80,.90,.95,.97,.98,.99],
    include='all',datetime_is_numeric=True)
print( d )

#import rasterio
#import rasterio.plot
#rast_src = r"/content/data/dem/N04E115.tif"
#with rasterio.open(rast_src) as src:
#    fig, ax = plt.subplots(figsize = (10,10))
#    rasterio.plot.show(src, ax=ax)

import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt
import contextily as ctx

fig = plt.figure(figsize=(16, 7))
ax = plt.subplot(111, frameon=False)

def gdfplot(df1,df2,df3,df4,df5):
    gdf1 = GeoDataFrame(df1, geometry=gpd.points_from_xy(df1.Longitud, df1.Latitud))
    gdf2 = GeoDataFrame(df2, geometry=gpd.points_from_xy(df2.Longitud, df2.Latitud))
    gdf3 = GeoDataFrame(df3, geometry=gpd.points_from_xy(df3.Longitud, df3.Latitud))
    gdf4 = GeoDataFrame(df4, geometry=gpd.points_from_xy(df4.Longitud, df4.Latitud))
    gdf5 = GeoDataFrame(df5, geometry=gpd.points_from_xy(df5.Longitud, df5.Latitud))
    # print(gdf.head())
    gdf1 = gdf1.set_crs('epsg:4326') # CRS84 is EPSG:4326
    gdf1 = gdf1.to_crs(epsg=3857)
    gdf2 = gdf2.set_crs('epsg:4326') # CRS84 is EPSG:4326
    gdf2 = gdf2.to_crs(epsg=3857)
    gdf3 = gdf3.set_crs('epsg:4326') # CRS84 is EPSG:4326
    gdf3 = gdf3.to_crs(epsg=3857)
    gdf4 = gdf4.set_crs('epsg:4326') # CRS84 is EPSG:4326
    gdf4 = gdf4.to_crs(epsg=3857)
    gdf5 = gdf5.set_crs('epsg:4326') # CRS84 is EPSG:4326
    gdf5 = gdf5.to_crs(epsg=3857)
    gdf1.plot( figsize=(16, 7), ax=ax, label='33-100',alpha=1.0, c='red', markersize=3)
    gdf2.plot( figsize=(16, 7), ax=ax, label='20-33',alpha=1.0, c='orange', markersize=3)
    gdf3.plot( figsize=(16, 7), ax=ax, label='10-20',alpha=0.5, c='green', markersize=3)
    gdf4.plot( figsize=(16, 7), ax=ax, label='2-10',alpha=1.0, c='blue', markersize=3)
    gdf5.plot( figsize=(16, 7), ax=ax, label='0-2', alpha=1.0, c='white', markersize=2)
    ctx.add_basemap(ax, crs=gdf5.crs.to_string(), source=ctx.providers.Esri.WorldImagery)
    return ax

superior = df.loc[ df['Prof(Km)'].between(33,100) ] # red
higher = df.loc[ df['Prof(Km)'].between(20,33) ] # orange
high = df.loc [ df['Prof(Km)'].between(10,20) ] # green
nominal = df.loc[ df['Prof(Km)'].between(2,10) ] # blue
low = df.loc[ df['Prof(Km)'].between(0,2) ] # white
other = df.loc[ df['Prof(Km)'].between(4,17) ] # blue
other2 = df.loc[ df['Prof(Km)'].between(0,8) ] # blue

d = other2.describe(percentiles=[.05,.10,.20,.25,.30,.40,.45,.50,.60,.70,.75,.80,.90,.95,.97,.98,.99],
    include='all',datetime_is_numeric=True)
print(d)
ax0 = gdfplot(superior,higher,high,nominal,low)

plt.legend(loc="upper right")
plt.show()
