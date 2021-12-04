# Acess to elevation maps
https://en-us.topographic-map.com/maps/df26/Atlantic-Ocean/
https://earthdata.nasa.gov/esdis/eso/standards-and-references/geotiff
https://lpdaac.usgs.gov/products/astgtmv003/
https://search.earthdata.nasa.gov/search?q=C1299783579-LPDAAC_ECS&m=28.518865105672898!-19.66552734375!7!1!0!0%2C2
https://lpdaac.usgs.gov/tools/appeears/
https://e4ftl01.cr.usgs.gov/
https://www.eorc.jaxa.jp/ALOS/en/aw3d30/
https://visibleearth.nasa.gov/images/57752/blue-marble-land-surface-shallow-water-and-shaded-topography
http://www.radcyberzine.com/xglobe/index.html#maps
http://www.naturalearthdata.com/downloads/10m-raster-data/10m-natural-earth-1/
https://mapcruzin.com/cloudmade-natural-earth-gadm-shapefiles/natural-earth-public-domain-shapefiles.htm
https://mapcruzin.com/free-world-country-arcgis-maps-shapefiles.htm

gdal_translate -a_srs WGS84 -a_ullr -180 +90 +180 -90 xglobe-2400.jpg xglobe-2400.tiff
