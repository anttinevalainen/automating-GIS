#import modules
import geopandas as gpd
import pandas as pd
from pyproj import CRS
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import contextily as ctx
import os


#read in grid area data (i'm using the grid only as a basemap)
fp = "data/TravelTimes_to_5975375_RailwayStation.shp"
grid = gpd.read_file(fp)
#read in road data from previous weeks
fp = "data/roads.shp"
roads = gpd.read_file(fp)
#read in csv data concerning road accidents in helsinki
fp = "data/liikenneonnettomuudet_Helsingissa.csv"
data = pd.read_csv(fp, sep=";", usecols=["pohj_etrs", "ita_etrs", "VAKAV_A", "VV"])


#prepare to convert the road accident data to geodataframe by creating column for geometry
data['geometry'] = None
geom = []
#go through the data row by row and making point data from the coordinates
for x, y in zip(data['ita_etrs'], data['pohj_etrs']):
    geom.append(Point(x, y))
#add point data in a list to the geometry column
data['geometry'] = geom

#convert pandas dataframe to geopandas geodataframe
geo = gpd.GeoDataFrame(data, geometry='geometry', crs=CRS.from_epsg(3879).to_wkt())

#reprojecting the point and road data to be that of the grid data
geo = geo.to_crs(grid.crs)
roads = roads.to_crs(grid.crs)



#########ASSERTION#########
assert geo.crs == roads.crs == grid.crs, 'gdf, road dataset and grid dataset crs should match'
###########################



#Start plotting

#reproject the car crash data to web mercator for a basemap
geo = geo.to_crs(epsg=3857)

#here i'm extracting only the crashes from year 2010 and above from the data
crash = geo.loc[(geo['VV'] >= 2010)]
#here i'm making a separate dataframe from only those crashes, where someone died
vakava = crash.loc[(crash['VAKAV_A'] == 3)]

#plotting the data with the basemap
fig, ax = plt.subplots(figsize=(12,8))
#here I'm creating a heatmap-ish effect by altering the points transparently (alpha)
    #more points, the darker the spot they manifest at is
crash.plot(ax=ax, markersize=3, color="black", alpha=0.03)
vakava.plot(ax=ax, markersize=3, color="red")
ctx.add_basemap(ax)

#control figure size in here
fig, ax = plt.subplots(figsize=(12,8))

#Change the basemap to dark carto map
carto = 'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'
crash.plot(ax=ax, markersize=3, color="lightgrey", alpha=0.03)
vakava.plot(ax=ax, marker="x", markersize=10, color="red")
#Set the basemap and add credit sources
ctx.add_basemap(ax,
                attribution = "Car crash data by City of Helsinki, Map Data © OpenStreetMap contributors",
                url=carto)

#Set extent
ax.set_xlim(2760000, 2800000)
ax.set_ylim(8430000, 8465000)
ax.set_title("2010-2018 data : Car crash clusters and spots of deadly car crashes in Helsinki")

#save the figure as png file
outfp1 = "docs/static_map.png"
plt.savefig(outfp1, dpi=300)

#save the figure as svg file
outfp2 = "docs/static_map.svg"
plt.savefig(outfp2, format='svg')


#########ASSERTION#########
assert os.path.isfile(outfp1), 'png-file does not exists in the filepath!'
assert os.path.isfile(outfp2), 'svg-file does not exists in the filepath!'
###########################
