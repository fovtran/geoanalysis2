import os
from osgeo import ogr
import pandas as pd
from shapely import wkt
import geopandas as gpd
import fiona

fiona.supported_drivers["OGR_GRASS"] = "r"
# gdf = gpd.read_file('/GRASSDB/LOCATION_NAME/MAPSET/vector/layername/head')

def grass2gpd(layername, grassdb, location_name, mapset):
    datafile = os.path.join(GRASSDB, LOCATION_NAME, MAPSET, 'vector', layername, 'head')
    driver = ogr.GetDriverByName('GRASS')
    # here the data is read in readonly mode, but also the GDAL GRASS driver has no write capabilities
    # I am not sure at the end of the method on how to properly close the datasource (and, actually, if I have to ... )
    dataSource = driver.Open(datafile, 0)
    layer = dataSource.GetLayer()
    srs = layer.GetSpatialRef().ExportToWkt()
    lyrDefn = layer.GetLayerDefn()
    fieldnames = []
    for i in range( lyrDefn.GetFieldCount() ):
        fieldnames.append(lyrDefn.GetFieldDefn(i).GetName() )
    # hack to avoid to call `layer.ResetReading()` and iterate again over the features
    #
    # I first build a list of dictionaries
    # each element of the list is of the form:
    # {geom: WKT_Geometry
    #  attr: {field_1: val, field_2: val, ..., field_N: val}}
    # So the attr key is a dictionary itself
    # the nested loop first get the feature then create a dictionary of attributes looping over the list of fields
    #
    wktgeom = [{'geom':feature.GetGeometryRef().ExportToWkt(),
                'attr':{i:feature.GetField(i) for i in fieldnames}} for feature in layer]
    # At this point I should close or unlink the datasource, but I can't find the right method to do it
    #
    # Create a dataframe from the list of dictionaries
    #
    df = pd.DataFrame(wktgeom)
    # convert the WKT string to a shapely WKT object
    # concatenate a Geometry dataframe with an attribute dataframe
    df_geom = pd.concat([df['geom'].apply(wkt.loads),
                        pd.DataFrame(list(df['attr'].values))],
                       axis=1, sort=False)
    # transform the pandas dataframe into a geopandas dataframe
    gdf = gpd.GeoDataFrame(df_geom, geometry='geom', crs=srs)
    return gdf

    GRASSDB="/home/epinux/Data/grassdata"
LOCATION_NAME="lonlat"
MAPSET="PERMANENT"

layername="img_left_filteredBS"

gdf = grass2gpd(layername=layername,
                grassdb=GRASSDB,
                location_name=LOCATION_NAME,
                 mapset=MAPSET)
type(gdf)

# returns
# geopandas.geodataframe.GeoDataFrame
