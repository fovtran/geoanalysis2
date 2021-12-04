# diego
import pandas as pd
pd.set_option('display.max_rows', 1000)
from numpy import array, ones, ma, meshgrid, where, exp

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

# print( df.describe() )
# Index(['Evento', 'Fecha', 'Hora', 'Latitud', 'Longitud', 'Prof.(Km)', 'Inten.', 'Mag.', 'TipoMag.', 'Localización'], dtype='object')
row = df.iloc[[0]]
indices = (df.index.tolist(), df.index.to_numpy())

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

gdf = GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud))
print(gdf.head())
#print(gdf.crs)
#world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# ax = world[world.continent == 'Africa'].plot(color='white', edgecolor='black')
#gdf.plot(ax=ax, color='red')

gdf = gdf.set_crs('epsg:4326') # CRS84 is EPSG:4326
gdf = gdf.to_crs(epsg=3857)

superior = gdf.loc[ gdf['Prof(Km)'] >35 ]
cond2 = gdf['Prof(Km)'].all() >=20 & gdf['Prof(Km)'].all() <=35
higher = gdf.loc[ cond2 ]
high = gdf.loc [ 20<gdf['Prof(Km)'].all() >10 ]
nominal = gdf.loc[ 2<gdf['Prof(Km)'].all() >10 ]
low = gdf.loc[ 0<gdf['Prof(Km)'].all() >10 ]

# group = gdf.groupby(pd.Grouper(key='DateTime', axis=1, freq='Y'))['Prof(Km)']
#x = [p.x for p in gdf['geometry'].values]
#ax = gdf.plot(kind='scatter', x=x, y=y, figsize=(16, 7), alpha=0.7, c=gdf['Mag'], s=gdf['Prof(Km)'], markersize=3)
ax = superior.plot(figsize=(16, 7), alpha=0.3, c='r', markersize=2)
higher.plot(figsize=(16, 7), alpha=0.3, c='o', markersize=2)
high.plot(figsize=(16, 7), alpha=0.3, c='g', markersize=2)
nominal.plot(figsize=(16, 7), alpha=0.3, c='b', markersize=2)
low.plot(figsize=(16, 7), alpha=0.3, c='k', markersize=2)
#ax = gdf.plot(figsize=(16, 7), alpha=0.3, c=gdf['Prof(Km)'], markersize=2)
ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)

X, Y = meshgrid(gdf.geometry.x, gdf.geometry.y)
#Z = ma.array(Z)
#Z[nominal] = ma.masked
#Z[low] = ma.masked
X = gdf.geometry.x
Y = gdf.geometry.y
Z =  gdf['Prof(Km)']
points = (X,Y)
grid_x , grid_y = meshgrid(X, Y)
from scipy.interpolate import griddata
#grid_z0 = griddata(points, Z, (grid_x, grid_y), method='nearest', rescale=True)
#grid_z1 = griddata(points, Z, (grid_x, grid_y), method='linear', rescale=True)
#grid_z2 = griddata(points, Z, (grid_x, grid_y), method='cubic', rescale=True)
origin = 'upper'
#cs = ax.contourf(grid_x, grid_y, grid_z1, 13, nchunk=6, levels=[0,1,2,10,11,12,13,14,33,34,43], hatches=['-', '/', '\\', '//'], cmap='jet', origin=origin, extend='both', alpha=0.009, corner_mask=True)
#ax.contour(cs, colors='k')
#im = plt.gca().get_children()[0]
#plt.colorbar(im, ax=ax, cmap='jet')
plt.show()

# import plotly.express as px
# fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, hover_name="Mag", zoom=1)
# fig.show()
