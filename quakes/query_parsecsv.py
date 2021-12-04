import pandas as pd
pd.set_option('display.max_rows', 1000)

from numpy import array, ones

filename = 'catalogoComunSV_1634534991274.csv'
df = pd.read_csv(filename, delimiter=';', skipinitialspace = True) #, parse_dates=[['Fecha', 'Hora']])
# list_of_rows = [list(row) for row in df.values]

for key in df.keys():
    newcolumnname = key.replace(' ', '').replace('.','')
    df = df.rename(columns={key: newcolumnname})

df = df.rename(columns={'Evento': 'i'})
df.set_index('i', inplace=True)
# df.columns = df.columns.str.replace(' ', '')

df.drop('TipoMag', axis=1, inplace=True)
df.drop('Inten', axis=1, inplace=True)

#df[["Fecha"]] = df[["Fecha"]].apply(pd.to_datetime)
#df['Fecha'] =  pd.to_datetime(df['Fecha'], format='%d%b%Y')
#df['Hora'] =  pd.to_datetime(df['Hora'], format='%H:%M:%S')
df["DateTime"] = df["Fecha"] + ' ' + df["Hora"]
df[["DateTime"]] = df[["DateTime"]].apply(pd.to_datetime)
df.drop('Hora', axis=1, inplace=True)
df.drop('Fecha', axis=1, inplace=True)

#print( df.keys() )
# Index(['Evento', 'Fecha', 'Hora', 'Latitud', 'Longitud', 'Prof.(Km)', 'Inten.', 'Mag.', 'TipoMag.', 'Localización'], dtype='object')
# print( df.describe() )
# row = df.iloc[[0]]
# print(row)
indices = df.index.tolist()
indices = df.index.to_numpy()
#print(indices)

# Bounding box
maxlat=28.984
minlon=-18.237
maxlon=-17.364
minlat=28.212
df = df.drop(df[df.Latitud <minlat].index)
df = df.drop(df[df.Latitud >maxlat].index)
df = df.drop(df[df.Longitud <minlon].index)
df = df.drop(df[df.Longitud >maxlon].index)

d = df.describe(percentiles=[.05,.10,.20,.25,.30,.40,.45,.50,.60,.70,.75,.80,.90,.95,.97,.98,.99],
    include='all',datetime_is_numeric=True)
print( d )

d = df[df.Mag >3.4].sort_values(['Localización', 'Mag', 'Prof(Km)'])
print(d)
