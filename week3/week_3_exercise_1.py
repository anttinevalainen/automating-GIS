import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from pyproj import CRS
import os
import requests
import geojson
import matplotlib.pyplot as plt


#GEOCODE SHOPPING CENTERS
#GEOCODE SHOPPING CENTERS

#import data through filepath to a dataframe called 'data'
fp = r'data/shopping_centers.txt'
data = pd.read_csv(fp, sep=';')

#geocode addresses using Nominatim.
geo = geocode(data['addr'], provider='nominatim', user_agent='autogis_an', timeout=4)

#reproject the crs
geo.crs #is epsg 4326
geo = geo.to_crs({'init': 'epsg:3879'})
geo.crs #is now epsg:3879

#make the join, store joined geodataframe to variable 'geodata'
geodata = geo.join(data)

#define output filepath
out_fp = r'data/shopping_centers.shp'
#save to Shapefile
geodata.to_file(out_fp)

#print info about output file
print("Geocoded output is stored in this file:", out_fp)
#check that the file exists in the fp
assert os.path.isfile(out_fp), "output shapefile does not exits"


#CREATE BUFFERS AROUND SHOPPING CENTERS
#CREATE BUFFERS AROUND SHOPPING CENTERS


#create a buffer column to geodata GeoDataFrame:
geodata['buffer'] = None

#Create buffer with the circumference of 3000m (radius of 1500m)
geodata['buffer'] = geodata.buffer(distance=1500)

#replace geometry with buffer
geodata['geometry'] = geodata['buffer']


#HOW MANY PEOPLE LIVE NEAR SHOPPING CENTERS?
#HOW MANY PEOPLE LIVE NEAR SHOPPING CENTERS?


#specify the filepath and parameters for wfs REQUEST
url = 'https://kartta.hsy.fi/geoserver/wfs'
params = dict(service='WFS', version='2.0.0', request='GetFeature', typeName='asuminen_ja_maankaytto:Vaestotietoruudukko_2018', 
              outputFormat='json')

#export the data using requests and the parameters created above
r = requests.get(url, params=params)

#move the request to a geodataframe 'Ppop'
pop = gpd.GeoDataFrame.from_features(geojson.loads(r.content))
pop = pop[['asukkaita', 'geometry']]

#classify the pop grid crs
pop.crs = CRS.from_epsg(3879)

#reclassify the geodata crs to wkt to match with population grid crs
geodata = geodata.to_crs(pop.crs)

#assertion check!
assert pop.crs == geodata.crs, 'the crs of pop and geodata geodataframes should match!'

#plot the population grids and geodata buffers to see what the spatial join is supposed to look like
#fig, ax = plt.subplots()
#geodata.plot(ax=ax, facecolor='teal')
#pop.plot(ax=ax, facecolor='beige')

#making a spatial join with only the grid squares completely within the buffer
join = gpd.sjoin(pop, geodata, how = 'inner', op = 'within')

#checking to see if the plotted spatial join looks ok
#join.plot()

#grouping the joined data by the name of a shopping center
grouped = join.groupby(by='name')

#form the print statement by looping each shopping center
for shopping_center, group in grouped:
    print('People living within 1,5 km radius of', shopping_center, ":", group['asukkaita'].sum())
