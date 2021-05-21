# Week 3

This week we will practice how to do geocoding, spatial joins and nearest neighbour analysis in Python.

In this exercise, the goal is to **find out how many people live within 1.5 km (Euclidian) distance from big shopping centers in Helsinki Region** (Exercise 1). In addition, you will figure out the closest shopping center from your home and work locations (Exercise 2).

## Exercises
- Exercise 1:
    - Geocode shopping centers
    - Create buffers around shopping centers
    - How many people live near shopping centers?
- Exercise 2:
    - What is the closest shopping center from your home / work?

## Exercise 1:

### Geocode shopping centers:

The overall aim of Exercise 1 is to find out **how many people live within a walking distance (1.5 km) from certain shopping centers in Helsinki**.

In problem 1 aim is to retreive numercal coordinates for the addresses of shopping centers. As an output, we will have a Shapefile which contains the geocoded result.

- Find out the addresses for following shopping centers from the internet, and write the addresses into a text file called `shopping_centers.txt`:
    - Itis
    - Forum
    - Iso-omena
    - Sello
    - Jumbo
    - REDI
    - Tripla

1.
`shopping_centers.txt` should have semicolon (`;`) as a separator, and the file should include the following columns:
- `id` (integer) containing an unique identifier for each shopping center
- `name` (string) of each shopping center
- `addr` (string) the address

2.
- Save (and upload) the text file into your repository.
- Read `shopping_centers.txt` into a DataFrame called `data`:
- Geocode the addresses using the Nominatim geocoding service. Store the output in a variable called `geo`
- Check that the coordinate reference system of the geocoded result is correctly defined, and **reproject the layer into ETRS GK-25**
- Make a table join between the geocoded addresses and the original addresses in order to link the numerical coordinates and  the `id` and `name` of each shopping center.
- Store the output in a variable called ``geodata``
- Save the output as a Shapefile called `shopping_centers.shp`

### Create buffers around shopping centers

Let's continue with our case study and calculate a buffer around the geocoded points.

1.
- Create a new column called `buffer` to `geodata` GeoDataFrame
- Calculate a 1.5 km buffer for each geocoded point. Store the buffer geometry in the new column
- Replace the values in `geometry` column with the values of `buffer` column
Optional: at this point, you can drop out unnecessary columns from the geodataframe. We will only need the columns `'id'`, `'name'` and `'geometry'`

### How many people live near shopping centers?

Last step in our analysis is to make a spatial join between our buffer layer and population data in order to find out **how many people live near each shopping center**. We will use **a Population Grid** that is available via the HSY wfs.

1.
- Read the population grid into a geodataframe, use only the useful columns: `'asukkaita'` (=population count per grid square) and `'geometry'`
- Make a spatial join between your buffered point layer and population grid layer.
- Group the joined layer by shopping center index
- Calculate the sum of population living within 1.5 km for each shopping center.

2.
- Print out the population living within 1.5 km from each shopping center:
    - Itis
    - Forum
    - Iso-omena
    - Sello
    - Jumbo
    - REDI
    - Tripla


**Reflections:**
- How challenging did you find problem 1 (on scale to 1-5), and why?
- What was easy?
- What was difficult?"

## Exercise 1:

### What is the closest shopping center from your home / work?

In the last problem you should find out the closest shopping center from two different locations a) your home and b) work place.

1.
- Create a txt-file called `activity_locations.txt` with two columns:
    - `id`: unique id for each row\n",
    - `addr`:  address of your work and home
- Save the text file into your repository.
- Read those addresses using pandas and geocode the addresses.
- Find out the nearest shopping center to these points using Shapely `nearest_points`.
- Print out the name of the shopping center that is nearest to a) home and b) work.


**Reflections:**
- How challenging did you find problem **1** (on scale to 1-5), and why?
- What was easy?
- What was difficult?"

**Can you think of other application cases for the nearest neighbour analysis?**

**Answers:**

**Exercise 1:**
- The problems were easier than last week, I'd rank the difficulty to 3, I still had to go to the group lecture to sort some of the things out on thursday! Working with multiple databases and tools may end up mixing up something in the middle, which i found out later on

- Grouping and making spatial joins with the data was easy

- Working with the grouped data was a bit more difficult. I'm trying to make use of different varibale names to make it more easy

**Exercise 2:**
- I could've added the shopping centers of Kamppi and Kämp Galleria to the list of shopping centers for this exercise, since I live next to Kamppi and work at Kämp Galleria..
- Nearest neigbor analysis is great for navigating through apps, which find the nearest bus stops etc. from the point you're located. Also, when searching for shops and businesses with multiple locations, a google search can find the nearest shop from the user's location, which is kind of neat!
- Nearest location can also be used when planning new business locations, to see the proximity of other businesses alike.

