# diego
import pandas as pd
pd.set_option('display.max_rows', 1000)
from numpy import array, ones, ma, meshgrid, where, exp

# accelerogramas la palma
# https://www.ign.es/web/ign/portal/sis-catalogo-acelerogramas/-/catalogo-acelerogramas/searchAcelerograma?latMin=28.212&latMax=28.984&longMin=-18.237&longMax=-17.364&startDate=01/01/2010&endDate=31/10/2021&selIntensidad=N&selMagnitud=N&intMin=&intMax=&magMin=&magMax=&selProf=N&profMin=&profMax=&cond=
# Sismos region palma
# https://www.ign.es/web/ign/portal/sis-catalogo-terremotos/-/catalogo-terremotos/searchTerremoto?latMin=26.6412193530742&latMax=30.244734978074202&longMin=-19.694437169627594&longMax=-15.212015294627593&startDate=01/01/2010&endDate=25/10/2021&selIntensidad=N&selMagnitud=N&intMin=&intMax=&magMin=&magMax=&selProf=N&profMin=&profMax=&fases=no&cond=
filename = 'acelerogramasComunSV_1635656334568.csv'
df = pd.read_csv(filename, delimiter=';', skipinitialspace = True) #, parse_dates=[['Fecha', 'Hora']])

for key in df.keys():
    newcolumnname = key.replace(' ', '').replace('.','')
    df = df.rename(columns={key: newcolumnname})

# df = df.rename(columns={'Evento': 'i'})
#df.set_index('i', inplace=True)
print ( df.describe() )
