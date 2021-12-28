# diego
from geoanalysistools.geo import *

df = gpd.read_file( 'data/lapalma-datetime-slice.geojson', driver="GeoJSON" )
df[["Date"]] = df[["Date"]].apply(pd.to_datetime)
gdf = GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud))

# 1.8-2.4 2.4-2.85 2.7-3.65 3.5-4.3 4.3-4.8 4.3 6
#q_none = gdf.loc[ df['magnitud'].between(1.8,2.4) ]
q_none = gdf.loc[ df['magnitud'].between(3.2,5.5) ]
profs = [
    (q_none['profundidad'].mean(), q_none['magnitud'].std(), q_none['profundidad'].std()),      # 1.8 - 2.4
     ]
other = [
    (q_none['profundidad'].mean(), q_none['magnitud'].kurtosis(), q_none['profundidad'].kurtosis()),  # 1.8 - 2.4
]
for p in profs:    print(p)
for q in other:    print(q)

df2 = pd.DataFrame( {'Vents': ['Vent 1'], 'Name': ['Dolly'], 'latitud': [28.58], 'longitud': [-17.84]} )

import mapclassify as mc

start_date = "2021-12-5"
end_date = "2021-12-27"
df1 = SeriesCutByDate(start_date, end_date, df)
m = mc.MaximumBreaks(df1.magnitud, k=8)
p1 = mc.MaximumBreaks(df1.profundidad, k=12, mindiff=4)

#print(m)
print(p1)
#print(p1.get_tss())
#print(p1.get_adcm())
#print(p1.get_gadf())
print(p1.get_legend_classes())
print(p1.counts)
print(dir(p1))
#print(p1.get_fmt())
#print(p1.bins)
#print(p1.y)
#print(p1.yb)
#print(p1.table())

start_date = "2021-10-1"
end_date = "2021-12-13"
df1 = SeriesCutByDate(start_date, end_date, df)
calc =['mean', 'min', 'max']
dates = df1.groupby(df1['Date'].dt.to_period('D'))
m = dates['magnitud'].agg(calc)
p = dates['profundidad'].agg(calc)
#print(m['max']>3.5)
e = pd.DataFrame({'Date':dates.size()})

#e = (dates.groupby(['magnitud', 'profundidad']).agg({
#    'magnitud': ['mean', 'count'],
#    'profundidad': ['median', 'min', 'count']
#    }))
#print(e)
