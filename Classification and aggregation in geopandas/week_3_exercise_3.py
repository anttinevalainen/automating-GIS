import pandas as pd
import geopandas as gpd
import requests
import geojson
from pyproj import CRS
import matplotlib.pyplot as plt

#create filepath for grid data and read the data into a geodataframe 'grid'
fp = r'data/P2_grid_data.shp'
grid = gpd.read_file(fp)

#specify the filepath and parameters for wfs from HSY
url = 'https://kartta.hsy.fi/geoserver/wfs'
params = dict(service='WFS', version='2.0.0', request='GetFeature',
              typeName='asuminen_ja_maankaytto:Vaestotietoruudukko_2018',
              outputFormat='json')
#export the data using requests and the parameters created above
r = requests.get(url, params=params)

#move the request to a geodataframe and name it 'pop', use only columns 'asukkaita' & 'geometry'
pop = gpd.GeoDataFrame.from_features(geojson.loads(r.content))
pop = pop[['asukkaita', 'geometry']]


#classify the pop grid crs as it is a no show. The crs used in the file is epsg 3879
pop.crs = CRS.from_epsg(3879)

#reclassify the grid.crs to match with pop.crs
grid = grid.to_crs(pop.crs)



#########ASSERTION#########
assert pop.crs == grid.crs, 'population grid and YKR grid crs should match'
###########################



#aggregate dominance areas into a unified geometries
dissolved = grid.dissolve(by='dominant_s')

#make a spatial join with grid squares that touch the dominant area of a shopping center
join = gpd.sjoin(pop, dissolved, how = 'inner', op = 'intersects')

#grouping the spatial join by the dominance area (one row for each shopping center)
grouped = join.groupby(by='index_right')


#here i'm creating a for loop, which prints out the name of each shopping center
#followed by the total population within its dominant area
for center, group in grouped:
    #i'm also splitting the name of the shopping center from index_right column to include only the name
    #sadly i had no name column in the data so iso omena is written together
    split = center.split('_')
    sc_name = split[-1]
    print('People living within the dominance area of', sc_name, "-", group['asukkaita'].sum())