
#import modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, MultiPoint
import matplotlib.pyplot as plt
from pyproj import crs
import osmnx as ox
from geopy.geocoders import Nominatim
import networkx as nx

#read the data
fp = "data/origins.csv"
orig = pd.read_csv(fp)
fp = "data/destinations.csv"
dest = pd.read_csv(fp)

#check the location by reverse geocoding one of the coordinates
address_string = dest['y'].at[0].astype(str) + ", " + dest['x'].at[0].astype(str)
location = Nominatim(user_agent="autogis_AN").reverse(address_string, timeout=10)
#print(location.address)
#is in Tallin, Estonia


#turn the origin and destination dataframes to geodataframes
#iterate the coordinates to point values
points = []
orig['geometry'] = None
for x, y in zip(orig['x'], orig['y']):
    points.append(Point(x, y))

#define the crs by the coordinates and make the convert
crs = {'init': 'epsg:4326'}
orig['geometry'] = points
orig = gpd.GeoDataFrame(orig, geometry='geometry', crs=crs)

#same for destination values
points = []
dest['geometry'] = None
for x, y in zip(dest['x'], dest['y']):
    points.append(Point(x, y))

dest['geometry'] = points
dest = gpd.GeoDataFrame(dest, geometry='geometry', crs=crs)



#########ASSERTION#########
assert orig.crs == dest.crs, 'origin and destination crs should match!'
###########################



#Making a geodataframe with all the points to form the convex hull of the area they cover
convex_points = orig.append(dest)

#Add 0.05 degree buffer to get all the streets in the network around the points
convex_points['buffer'] = None
convex_points['buffer'] = convex_points.buffer(0.05)
convex_points['geometry'] = convex_points['buffer']

#[xmin, ymin, xmax, ymax]
#[[xmin, ymax], [xmin, ymin], [xmax, ymin], [xmax, ymax]]
#create bounding box for the dataframe
bounding = [(24.4598, 59.5912), (24.4598, 59.2224), (24.9921, 59.2224), (24.9921, 59.5912)]
graph_extent = Polygon(shell=bounding)

#fetch the network data of drivable streets
graph = ox.graph_from_polygon(graph_extent, network_type='drive')

#project the graph and its nodes and edges
graph_proj = ox.project_graph(graph)
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)

#reproject the data pieces to the same crs as above
orig = orig.to_crs(nodes_proj.crs)
dest = dest.to_crs(nodes_proj.crs)
print(dest.crs)
print(orig.crs)
print(nodes_proj.crs)
print(edges_proj.crs)



#########ASSERTION#########
assert (orig.crs == dest.crs ==
        nodes_proj.crs == edges_proj.crs), 'crs should match on all dest, orig, nodes and edges!'
###########################



#plot the street data along with the origin and destination points
fig, ax = plt.subplots(figsize=(8,16))
orig.plot(ax=ax, color = 'red')
dest.plot(ax=ax, color= 'blue')
edges_proj.plot(ax=ax, color='gray', linewidth=0.5, alpha=0.7)
#image can be found in the img -folder


#########EXERCISE 2#########


#Start creating the shortest paths
routes = []

for i, origin in orig.iterrows():

    #define nearest node for the origin points
    orig_alt = ox.get_nearest_node(graph_proj, (origin.geometry.y, origin.geometry.x), method='euclidean')
    for j, destin in dest.iterrows():

        #define nearest node for the destination points
        dest_alt = ox.get_nearest_node(graph_proj, (destin.geometry.y, destin.geometry.x), method='euclidean')

        #define the shortest path from each origin to each destination
        route = nx.shortest_path(G=graph_proj, source=orig_alt, target=dest_alt, weight='length')
        if len(route) >= 2:
            routes.append(route)

#form the net geodataframe from the list created in the nested for-loops above
routes = gpd.GeoDataFrame()
routes['node_paths'] = routes

#make the geometry column for the routes-geodataframe
routes['geometry'] = None

for i, row in routes.iterrows():
    #get linestring objects from the routes in the dataframe, apply as geometry
    route_nodes = nodes_proj.loc[row['node_paths']]
    route_line = LineString(list(route_nodes.geometry.values))
    routes['geometry'].loc[i] = route_line


#create route_dist column and calculate the distances for each route
routes['route_dist'] = None
for index, row in routes.iterrows():
    routes['route_dist'].loc[index] = routes['geometry'].loc[index].length

#plot the data
fig, ax = plt.subplots(figsize=(8,16))
orig.plot(ax=ax, color='orange')
dest.plot(ax=ax, color= 'blue')
routes.plot(ax=ax, linewidth=1.0, color='red')
edges_proj.plot(ax=ax, color='gray', linewidth=0.5, alpha=0.7)
#image can be found in the img folder

#calculate the total distance of all the routes
total_distance = 0
for index, row in routes.iterrows():
    total_distance = total_distance + routes['route_dist'].loc[index]

print("Total distance of all the routes: ", round(total_distance/1000, 2), "km")

#########ASSERTION#########
assert round(total_distance /1000) == 2477, "total distance does not match the answer"
###########################
