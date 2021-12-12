import os
import pandas as pd
pd.set_option('display.max_rows', 1000)
pd.set_option('display.float_format', '{:.3f}'.format)

from geopandas import GeoDataFrame, read_file
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.animation import MovieWriter
import contextily as ctx
import numpy as np
from numpy import array, ones, ma, meshgrid, where, exp, matrix
from numpy import nan, nan_to_num,array,multiply,round, number
import urllib
from datetime import datetime, timedelta
import toml

def readconf(filename):
    data = toml.load(filename)
    print (data.keys())
    return data

def clearspacesdataframe(df):
    for key in df.keys():
        newcolumnname = key.replace(' ', '').replace('.','')
    return df.rename(columns={key: newcolumnname})

def todayDate():
    day = datetime.today().day
    month = datetime.today().month
    year = datetime.today().year
    return str(day) + '/' + str(month) + '/' +  str(year)

def todayDate2():
    day = datetime.today().day
    month = datetime.today().month
    year = datetime.today().year
    return str(year) + '-' + str(month) + '-' +  str(day)

def color_map_color(value, cmap_name='viridis', vmin=0.0, vmax=6.0):
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    rgb = cmap(abs(value))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color

def SeriesCutByDate(start_date, end_date, dframe):
    # Somethin's wrong with the series from GeonJSON.
    df2 = dframe.copy()
    after_start_date = df2["Date"] >= pd.to_datetime(start_date,infer_datetime_format=False, format='%Y/%m/%d')
    before_end_date = df2["Date"] <= pd.to_datetime(end_date,infer_datetime_format=False, format='%Y/%m/%d')
    between_two_dates = after_start_date & before_end_date
    return df2.loc[between_two_dates]

def saveGeoJsonSlice(df, start_date, end_date, filename):
    df2 = SeriesCutByDate(start_date, end_date, df.copy())
    df2.to_file(filename, driver="GeoJSON")

#series = RaceDataSeries(dataframe=df, params=seism_params, depth_key='profundidad').get_one('nominal').index
#for idx in series:
#    mag = df.loc[idx].magnitud
