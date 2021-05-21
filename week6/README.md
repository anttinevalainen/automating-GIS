# Exercise 6

Practicing how to work with OpenStreetMap data and conduct network analysis in Python.

## Problem 1 (8 points)

There are two csv-files in the data-folder:
- `origins.csv`
- `destinations.csv`

The files contain coordinates of the origin and destination points in certain area of the world as latitude and longitude coordinates (decimal degrees).

### 1.
Find out where the points are located based on the coordinates found in the files (which city/country?) Use your GIS skills to find out the solution in two different ways:

A. detect the location using **visualization techniques**; plot the points on top of a background map and see where they are located!

B. Detect the location using **geocoding techniques**; reverse geocode at least one of the locations. As output, you should print out information about the location (can be a full address, or just the name of the city)

### 2.
Retrieve OpenStreetMap data (streets that can be driven with car) from the area.**

- First, specify the extent for downloading the graph as a polygon.
    - Note that some of the routes might go beyond the extent of the point data sets

- Use the polygon to fetch the drivable network data
- store the street network a variable called `graph`

### 3.
Reproject the data into UTM projection, and plot:

- the street network (with `gray` color and line width of `0.5` and alpha set to `0.7`)
- the origin points (with `red` color)
- destination points (with `blue` color)


## Problem 2 Conducting shortest path routing


### 1.
Calculate the shortest paths between all origin points (16) and destination points (20). Use the `distance` of the road segments as the impedance measure

- To be able to find the shortest paths, find the nearest nodes from the graph for both origin and destination points.
- If the closest node is the same for both origin and destination point, skip the shortest path calculation.
- After the routing, add the shortest path routes as LineString geometries into a GeoDataFrame called `routes`
- Use the projected graph as the network for the analyses


### 2.
Calculate the distance of the routes into a new column called `route_dist`


### 3.
Plot all the routes on top of the street network.


### 4.
Calculate the total distance of all the routes. Update the `total_distance` based on your calculations.


