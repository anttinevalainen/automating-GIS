# Week 1: Working with Geometric Objects
# Exercise 1:

Practicing how to create geometric objects using Shapely module and how to find out different useful attributes from those geometries. Creating small functions that I can reuse later on when continuing with GIS analysis in Python.

## Problem 1: Creating basic geometries

1: Create a function called `create_point_geom()` that has two parameters `(x_coord, y_coord)`. Function should create a shapely `Point` geometry object and return that.

2: Create a function called `create_line_geom()` that takes a list of Shapely Point objects as parameter called `points` and returns a LineString object of those input points. In addition, you should take care that the function is used as it should
    - Inside the function, you should first check with `assert` -functionality that the input is a list If something else than a list is passed for the function, you should return an Error message: `\"Input should be a list!\"`
    - You should also check with `assert` that the input list contains at least two values. If not, return an Error message: `\"LineString object requires at least two Points!\"`
    - Optional: Finally, you should check with `assert` that all values in the input list are truly Shapely Points. If not, return an Error message: `\"All list values should be Shapely Point objects!\"`

3: Create a function called `create_poly_geom()` that has one parameter called `coords`. `coords` parameter should containt a list of coordinate tuples. The function should create and return a Polygon object based on these coordinates.
    - Inside the function, you should first check with `assert` -functionality that the input is a list. If something else than a list is passed for the function, you should return an Error message: `\"Input should be a list!\"`
    - You should also check with `assert` that the input list contains at least three values. If not, return an Error message: `\"Polygon object requires at least three Points!\"`
    - Check with `assert` that the data type of the objects in the input list. All values in the input list should be tuples. If not, return an error message: `\"All list values should be coordinate tuples!\"`

## Problem 2: Attributes of geometries

1: Create a function called `get_centroid()` that has one parameter called `geom`. The function should take any kind of Shapely's geometric -object as an input, and return a centroid of that geometry. In addition, you should take care that the function is used as it should:
    - Inside the function, you should first check with `assert` -functionality that the input is a Shapely Point, LineString or Polygon geometry. If something else than a list is passed for the function, you should return an Error message: `\"Input should be a Shapely geometry!\"`

2: Create a function called `get_area()` with one parameter called `polygon`. Function should take a Shapely's Polygon -object as input and returns the area of that geometry.
    - Inside the function, you should first check with `assert` -functionality that the input is a Shapely Polygon geometry. If something else than a list is passed for the function, you should return an Error message: `\"Input should be a Shapely Polygon -object!\"`

3: Create a function called `get_length()` with parameter called `geom`. The function should accept either a Shapely LineString or Polygon -object as input. Function should check the type of the input and returns the length of the line if input is LineString and length of the exterior ring if input is Polygon. If something else is passed to the function, you should return an `Error` `\"'geom' should be either LineString or Polygon!\"` (Use assert functionality).

4: Demonstrate your use of DocString with a single print statement

# Exercise 2:

## Problem 3: Reading coordinates from a file and creating geometries

One of the most typical problems in GIS is the situation where you have a set of coordinates in some file, and you need to map those. Python is a really handy tool for these kind of situations, as it is possible to read data from (basically) any kind of input datafile (such as csv-, txt-, excel-, gpx-files (gps data), databases etc.).

Thus, let's see how we can read data from a file and create Point -objects from them that can be saved e.g. as a new Shapefile. Our dataset **[travelTimes_2015_Helsinki.txt](data/travelTimes_2015_Helsinki.txt)** consist of travel times between specific locations in Helsinki Region. The first four rows of our data looks like this:

`from_id;to_id;fromid_toid;route_number;at;from_x;from_y;to_x;to_y;total_route_time;route_time;route_distance`
`5861326;5785640;5861326_5785640;1;08:10;24.9704379;60.3119173;24.8560344;60.399940599999994;125.0;99.0;22917.6`
`5861326;5785641;5861326_5785641;1;08:10;24.9704379;60.3119173;24.8605682;60.4000135;123.0;102.0;23123.5`
`5861326;5785642;5861326_5785642;1;08:10;24.9704379;60.3119173;24.865102;60.4000863;125.0;103.0;23241.3`

As we can see, there exists many columns in the data, but the few important ones needed here are:

| Column | Description |
|--------|-------------|
| from_x | x-coordinate of the **origin** location (longitude) |
| from_y | y-coordinate of the **origin** location (latitude) |
| to_x   | x-coordinate of the **destination** location (longitude)|
| to_y   | y-coordinate of the **destination** location (latitude) |
| total_route_time | Travel time with public transportation at the route |

Read more about the input data set at the Digital Geography Lab / Accessibility Research Group (University of Helsinki, Finland) website: https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/ .

### Steps
1: Read the [data/travelTimes_2015_Helsinki.txt](data/travelTimes_2015_Helsinki.txt) file into a variable **`data`** using  pandas
**NOTE:** What is the separator in the data (see above)? Remember to take that into account when reading the data.

2: Select the 4 columns that contain coordinate information (**'from_x'**, **'from_y'**, **'to_x'**, **'to_y'**) and store them in variable **`data`** (i.e. update the data -variable).

3: Create (two) empty lists for points called **`orig_points`** and **`dest_points`**\n"

4: Create shapely points for each origin and destination and add origin points to `orig_points` list and destination points to `dest_points` list.

## Problem 4: Creating LineStrings that represent the movements

1: Create the following functions
    - `create_od_lines()`: Takes two lists of Shapely Point -objects as input and returns a list of LineStrings\n",
    - `calculate_total_distance()`: Takes a list of LineString geometries as input and returs their total length\n",
2: Apply the functions to the dataset with the help of the functions formed in the previous steps
3: Create a print statement for the outputs of the functions and define the total distance of the points in the **[travelTimes_2015_Helsinki.txt](data/travelTimes_2015_Helsinki.txt)** dataset
