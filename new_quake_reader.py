# diego
from geoanalysistools import *

df = gpd.read_file( 'data/lapalma-datetime-slice.geojson', driver="GeoJSON" )
df[["Date"]] = df[["Date"]].apply(pd.to_datetime)
gdf = GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud))

# 1.8-2.4 2.4-2.85 2.7-3.65 3.5-4.3 4.3-4.8 4.3 6
q_none = gdf.loc[ df['magnitud'].between(1.8,2.4) ]
profs = [
    (q_none['profundidad'].mean(), q_none['magnitud'].std(), q_none['profundidad'].std()),      # 1.8 - 2.4
     ]
other = [
    (q_none['profundidad'].mean(), q_none['magnitud'].kurtosis(), q_none['profundidad'].kurtosis()),  # 1.8 - 2.4
]
for p in profs:    print(p)
for q in other:    print(q)

df2 = pd.DataFrame( {'Vents': ['Vent 1'], 'Name': ['Dolly'], 'latitud': [28.58], 'longitud': [-17.84]} )
