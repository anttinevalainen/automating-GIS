import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from pyproj import CRS
import os
from shapely.geometry import Polygon, LineString, Point

#export the data to a dataframe variable 'data'. Specify the empty geometry column
fp = r'data/some_posts.csv'
data = data = pd.read_csv(fp)
data['geometry'] = None

#new list for geometries
geometry = []

#loop the lat/lon columns to create geometric point objects, add them to the list created above
for lon, lat in zip(data['lon'], data['lat']):
    geometry.append(Point(lon, lat))

#specify the geometry-list as the geometry column in the dataframe
data['geometry'] = geometry

#test prints
print("Number of rows:", len(data))
print(data['geometry'].head())

#convert to geodataframe
geo = gpd.GeoDataFrame(data, geometry='geometry', crs=CRS.from_epsg(4326).to_wkt())

#save the GeoDataFrame into a new Shapefile
fp = 'data/kruger_posts/kruger_posts.shp'
geo.to_file(fp)

#test prints
print("Number of rows:", len(geo))
print(geo.head())

#check file exists in fp
assert os.path.isfile(fp), "output shapefile does not exist"

#plotting the data
geo.plot()

#The finished map of points has been saved to data as kruger_some_points.png