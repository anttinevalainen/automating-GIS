import pandas as pd
import geopandas as gpd
from geopandas.tools import geocode
from pyproj import CRS
import matplotlib.pyplot as plt
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points

# read in input files
fp1 = r'data/activity_locations.txt'
data_home = pd.read_csv(fp1, sep=';')
fp2 = r'data/shopping_centers.txt'
data_shopping = pd.read_csv(fp2, sep=';')

# Geocode activity locations
homework_geocode = geocode(data_home['addr'], provider='nominatim', user_agent='autogis_an', timeout=10)
shopping_geocode = geocode(data_shopping['addr'], provider='nominatim', user_agent='autogis_an', timeout=10)

#join the end results to get the columns from the original dataframes
homework = homework_geocode.join(data_home)
shopping = shopping_geocode.join(data_shopping)

#check crs
assert homework.crs == shopping.crs, 'the homework and shopping geodataframe crs should match'

#plotting the spots for home and work and the shopping centers in a single plot
#fig, ax = plt.subplots()
#shopping.plot(ax=ax, facecolor='k')
#homework.plot(ax=ax, facecolor='salmon')

#form a function to calculate nearest points.
def get_nearest_values(row, other_gdf, point_column='geometry', value_column="geometry"):
    '''Finds the nearest point from other geodataframe and return the
    corresponding value from specified value column in the given
    geodataframe.

    Args:
        row: The new row in given geodataframe the function is applied to
        other_gdf: The geodataframe the function compares the input gdf to
        point_column: The column of geometry from the input gdf
        value_column: The column of geometry from the compare gdf

    Returns:
        nearest_value:
    '''

    #create an union of the other GeoDataFrame's geometries:
    other_points = other_gdf["geometry"].unary_union

    #find the nearest points
    nearest_geoms = nearest_points(row[point_column], other_points)

    #get corresponding values from the other df
    nearest_data = other_gdf.loc[other_gdf["geometry"] == nearest_geoms[1]]

    nearest_value = nearest_data['name'].get_values()[0]

    return nearest_value

#Apply the function above
homework["nearest_loc"] = homework.apply(get_nearest_values,
                                         other_gdf = shopping,
                                         point_column = "geometry",
                                         axis = 1)

#End result printing
print('Shopping center closest to home:', homework['nearest_loc'].get_values()[0])
print('Shopping center closest to work:', homework['nearest_loc'].get_values()[1])
