import geopandas as gpd
import pandas as pd
import os
import matplotlib.pyplot as plt
from pyproj import CRS
from shapely.geometry import Polygon, LineString, Point

#read the file
fp = "kruger_posts/Kruger_posts.shp"
data = gpd.read_file(fp)

#check the crs and reproject the data to EPSG:32735
data.crs
data = data.to_crs(epsg=32735)

#test prints
print(data.head())
print(data.crs)

#Updating the data to be grouped by unique user ids
grouped = data.groupby(by='userid')

#check that the number of groups and unique user ids match
assert len(grouped.groups) == data["userid"].nunique(), "Number of groups should match number of unique users!"


#creating new geodataframe with specified index of userids, i also made sure that the crs stays the same
movements = gpd.GeoDataFrame(index = data['userid'].unique(), crs={'init' :'epsg:32735'})

#adding empty column for geographies
movements['geometry'] = None

#loop the geodataframe by unique user id.
#i'm creating the linestrings if a user has more than one some post.
#these lines are added to the movements GeoDataFrame
for user, group in grouped:
    groupx = group.sort_values(by='timestamp')
    if (len(groupx) > 1):
        line = LineString(groupx['geometry'].values)
        movements.at[user, 'geometry'] = line

#Check crs
print(movements.crs)

#Add new column for the distances of each line
movements['distance'] = movements['geometry'].length

#prints to answer the questions in the markdown
print('max:', round(movements['distance'].max(), 2), 'meters')
print('min:', round(movements['distance'].min(), 2), 'meters')
print('mean:', round(movements['distance'].mean(), 2), 'meters')

#Saving the shp files to a specific folder
fp = 'data/some_movements/some_movements.shp'
movements.to_file(fp)

#I ALSO CREATED A VERY QUICK MAP TO SEE IF THE OUTPUT WAS WHAT I THOUGHT IT WOULD BE.
#I inserted the map in the markdown.

#check that the file exists in the fp
assert os.path.isfile(fp), "output shapefile does not exits"