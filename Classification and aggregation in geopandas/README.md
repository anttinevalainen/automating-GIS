# Week 4

This week we will practice how to do data classification and aggregation in Geopandas. In this exercise we use data from the [Helsinki Region Travel Time Matrix](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix/) as input.

The overall aim is to define dominance areas for 8 shopping centers in Helsinki with different travel modes. The last step is to find out how many people live within the dominance areas of those big shopping centers in Helsinki Region.

# Exercises
- Exercise 1: Join accessibility datasets into a grid and visualize them by using a classifier
- Exercise 2: Calculate and visualize the dominance areas of shopping centers
- Exercise 3: How many people live under the dominance area of each shopping center

## Exercise 1: Join accessibility datasets into a grid and visualize them by using a classifier

**Data:**
- Travel time data: `travel_times_to_[XXXXXXX]_[NAME-OF-THE-CENTER].txt`
- Reference grid: `MetropAccess_YKR_grid_EurefFIN.shp`

1.
The goal is to visualize travely times by public transport and car to both shopping centers. Before plotting the maps you need to classify the data. The task is to develop the processing steps using Itis as input, and repeat the steps for Myyrmanni.

- Read the Polygon grid `MetropAccess_YKR_grid_EurefFIN.shp` into a GeoDataFrame called `grid`
- Read the travel time data file for Itis using Pandas into a variable called `data`
- Select only following columns from the file:
    - `pt_r_t`
    - `car_r_t`
    - `from_id`
    - `to_id`
- join attributes from `data` to `grid`, store the join output into a variable called `data_geo`
- Remove all rows containing no-data values (-1) from `data_geo`.
- Classify the travel times for both travel modes (public transport and private car) into five-minute intervals

2.
Create a plot where the you plot travel times by public transport and by car to Itis:

- Create subplots, the figure size should be 10 inches by 5 inches
- Add titles for the subplots
- Save the figure into the repository with filename `itis_accessibility.png`

**Repeat the steps for Myyrmanni**

**Optional: 4-panel figure**

Plot travel times to Itis and Myyrmanni all in one 4-panel figure.

- save the figure as `shopping_center_accessibility.png`


## Problem 2: Calculate and visualize the dominance areas of shopping centers

In this problem, the aim is to define the dominance area for each of the given shopping centers based on public transport travel time.

### Data
- A dataset contains 7 text files having data about accessibility in Helsinki Region, and a Shapefile that contains a Polygon grid.
    - `travel_times_to_[XXXXXXX]_[NAME-OF-THE-CENTER].txt` including travel times and road network distances to a specific shopping center
    - `MetropAccess_YKR_grid_EurefFIN.shp`


### An overview of the problem

In this problem you want to identify the closest shopping center for each grid cell in the region by public transport, and to visualize dominance areas for each shopping center based on this information.

1.
Combine public transport travel time information from all input files into one GeoDataFrame.

- rename the travel time columns so that they can be identified.
- Join those columns into the grid shapefile.
- At the end you should have one GeoDataFrame with different columns showing the travel times to different shopping centers.


2.
Find out the closes shopping center for each grid cell in the region

- For each grid cell, find out the minimum time across all travel time columns and insert that value into a new column called `min_t`.
- Figure out which column contains the minimum travel time using `idxmin()` function and parse information about the closest shopping center into a column called `dominant_service`.


3.
Visualize the dominance areas and travel times
- Visualize the dominance areas
- Visualize travel times to shopping centers
- Create subplots with 2 rows and one column

**Upload all your work into your own repository.**


### Steps

1.
- Fetch the filepaths to all textfiles found in data directory
- Automatically read all the files into a list called `filepaths`
- Read the YKR grid shapefile into a variable called `grid`
- Join information from all the input layers into the grid. As output, you should have a GeoDataFrame that contains the YKR_ID, grid geometry, and travel times to each shopping center. You should have (at least) 9 columns in the merged output:
    - `'YKR_ID'`
    - `'pt_r_t_Jumbo'`
    - `'pt_r_t_Dixi'`
    - `'pt_r_t_Myyrmanni'`
    - `'pt_r_t_Itis'`
    - `'pt_r_t_Forum'`
    - `'pt_r_t_IsoOmena'`
    - `'pt_r_t_Ruoholahti'`
    - `'geometry'`.

2.
- Remove rows containing no-data -values
- For each grid cell, find out the shortest travel time to any shopping center. Store the result in a new column `'min_t'`.

3.
- Find out also the column name for the shortest travel time using the `idxmin()` function into a column called `'dominant_service'`
- Visualize the dominance areas and travel times in one figure which has 2 subplots (2 rows and one column):
    - visualize the dominance areas using the names found in `dominant_service` column.
    - Visualize travel times to shopping centers from the `min_t` column


## Exercise 3: How many people live under the dominance area of each shopping center?

Find out how many people live under the dominance area of each shopping center.

- Aggregate your dominance areas into a unified geometries in Geopandas before joining with the population data
- Make the spatial join using `intersect`as the condition
