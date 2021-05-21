# Week 2

Creating geometries, reproject data and doing geometric calculations using Geopandas (+ Shapely and pyproj).

## Exercises

 - Exercise 1: Create Polygon from lists of coordinates
 - Exercise 2: Points to map
 - Exercise 3: How long distance individuals have travelled?

## Exercise 1: Create Polygon from lists of coordinates
In the first problem you should create a polygon based on the provided coordinates, and plot the polygon on a map.

Two lists; `longitudes` and `latitudes` contain the input coordinates for the polygon. The first coordinate pair looks like this: `(29.99671173095703, 63.748023986816406)`.

- Create a Polygon variable poly based on the coordinates
- Insert the polygon into a GeoDataFrame called geo:
- Plot the polygon. Note: you might need to call matplotlib pyplot show() -method in order to display the map
- Save the GeoDataFrame into a Shapefile called 'polygon.shp'

## Exercise 2: Points to map
The problem 2 this week continues the process that we started last week in Exercise 1, i.e. creating geometric point -objects and putting them into a map.

In this problem, our aim is to plot a map based on a set of longitude and latitude coordinates that are stored in a csv file. The coordinates are in WGS84 decimal degrees, and the data is stored in `some_posts.csv` CSV file in the data folder. First rows of the data look like this:

`lat,lon,timestamp,userid`
`-24.980792492,31.484633302,2015-07-07 03:02,66487960`
`-25.499224667,31.508905612,2015-07-07 03:18,65281761`
`-24.342578456,30.930866066,2015-03-07 03:38,90916112`
`-24.85461393,31.519718439,2015-10-07 05:04,37959089`
The data has 81379 rows and consists of locations and times of social media posts inside Kruger national park in South Africa:
| Column | Description |
|--------|-------------|
| lat_y | coordinate of the post |
| lon_x | coordinate of the post |
| timestamp   | Time when the post was uploaded|
| userid   | unique user ID |
Note: although the data is based on real social media data, it is heavily anonymized. Userids and timestamps have been randomized, i.e. they do not not match with real ones, also spatial accuracy of the data has been lowered.

1.
- Import the needed modules
- Read the data from `data/some_posts.csv` into a Pandas dataframe called data
- Create an empty column called geometry where you will store shapely Point objects
- Insert Point objects into the column geometry based on the coordinate columns
- Save the result as a shapefile:

2.
- Convert that DataFrame into a GeoDataFrame called `geo`
- Update the CRS for coordinate system as WGS84 (i.e. epsg code: 4326) in the WKT format
- Save output to file: `Kruger_posts.shp`
- Create a simple map of the points using the `geodataframe.plot()` -funtion. You might need to use the `matplotlib pyplot show()` method to display the image within this notebook.

Optional: Download the output shapefile and create a map in a gis-software (for example, overlay the points with a basemap). If you do this, remember to upload the map as a png image to this repository and add link to the image file to this markdown:

## Exercise 3: How long distance individuals have travelled?

In this problem the aim is to calculate the distance in meters that the individuals have travelled according the social media posts (Euclidean distances between points). In this problem, we will need the `userid` -column an the points created in the previous problem. You will need the shapefile `Kruger_posts.shp` generated in Problem 2 as input file.

Our goal is to answer these questions based on the input data:
- What was the shortest distance travelled in meters?
- What was the mean distance travelled in meters?
- What was the maximum distance travelled in meters?

1.
- Read in the shapefile as a geodataframe called `data`
- Check the crs of the input data. If this information is missing, set it as WGS84
- Reproject the data from WGS84 to UTM zone for South Africa to transform the data into metric system. (update the existing variable!)
- Group the data by userid

2.
- Create an empty GeoDataFrame called `movements`
- Iterate over the grouped object. For each user's data:
    - Sort the rows by timestamp 
    - Create a LineString object based on the user's points
    - Add the geometry and the userid into the `movements` dataframe.
- Set the CRS of the `movements` GeoDataFrame as `EPSG:32735`
- Check the crs definition of your dataframe (define the correct crs if this information is faulty or missing)
- Calculate the lenghts of the lines into a new column called `distance` in `movements` GeoDataFrame.

You should now be able to print answers to the following questions:
- What was the shortest distance travelled in meters?
- What was the mean distance travelled in meters?
- What was the maximum distance travelled in meters?

Finally, save the movements of into a Shapefile called `some_movements.shp`
