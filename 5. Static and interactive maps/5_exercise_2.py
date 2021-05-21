#import modules
import geopandas as gpd
import pandas as pd
from pyproj import CRS
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import contextily as ctx
import mplleaflet
import folium

#Reading regional population data from 2018 by statistics finland
fp1 = "data/001_11ra_2018.csv"
data2018 = pd.read_csv(fp1, sep=';')

#reading regional estimates for population in 2040 by statistics finland
fp2 = "data/003_128v_2040.csv"
data = pd.read_csv(fp2, sep=';')

colnames = {'alue' : 'nimi'}
data2018.rename(columns=colnames, inplace=True)
data.rename(columns=colnames, inplace=True)

#reading the geojson data of regional boundaries
url = "http://geo.stat.fi/geoserver/tilastointialueet/wfs?request=GetFeature&typename=tilastointialueet:maakunta1000k_2018&outputformat=JSON"
geodata = gpd.read_file(url)
geodata = geodata[['vuosi', 'nimi', 'maakunta', 'geometry']]


#calculating the change in population for each region
data['muutos'] = None
data['2018'] = None
delta = []
d2018 = []

#go through the population in 2018 and 2040 population estimate dataframes
for x, y in zip(data2018['vaesto2018'], data['vaesto2040']):
    change = (y - x) / x * 100
    d2018.append(x)
    delta.append(round(change, 2))
#Adding the change in population to the 2040 dataframe
data['muutos'] = delta
data['2018'] = d2018


#i had troubles with matching the region names in the dataframes because the geodataframe contained alot of whitespace
#here i'm using strip-function to get rid of all the whitespace around the name of the region
for index, row in geodata.iterrows():
    geodata['nimi'].at[index] = geodata['nimi'].at[index].strip()

#print info
print("Count of original attributes:", len(data))
print("Count of original geometries:", len(geodata))
# Merge data
geodata = geodata.merge(data, on = "nimi")
#Print info
print("Count after the join:", len(geodata))


#define geoid for folium mapping
geodata['geoid'] = geodata.index.astype(str)

#creating interactive map
map = folium.Map(location=[64.96, 27.59],
                 tiles = 'cartodbpositron',
                 zoom_start=5,
                 control_scale=True)

folium.Choropleth(geo_data = geodata,
                  data = geodata,
                  columns=['geoid','muutos'],
                  key_on='feature.id',
                  fill_color='RdYlBu',
                  line_color='white',
                  line_weight=0,
                  legend_name= 'Change in population (%)').add_to(map)

#adjusting the popups for the folium map
folium.features.GeoJson(geodata,
                        name='Labels',
                        style_function = lambda x: {'color':'transparent',
                                                    'fillColor':'transparent',
                                                    'weight':0},
                        tooltip = folium.features.GeoJsonTooltip(fields = ['muutos'],
                                                                aliases = ['Regional change in population between 2018 and 2040'],
                                                                labels=True,
                                                                sticky=False
                                                                            )
                       ).add_to(map)

#save the map to the repository
outfp = "docs/population_change.html"
map.save(outfp)
