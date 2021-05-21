from typing import Tuple
from shapely.geometry import Point, LineString, Polygon

def create_point_geom(x_coord, y_coord):
    '''Creates a Point formed from the input x and y coordinates

    Args:
        x_coord: Float value representing the x coordinate of the output point
        y_coord: Float value representing the y coordinate of the output point

    Returns:
        Point(x_coord, y_coord): Point variable formed from the input coordinates
    '''
    assert type(x_coord) == float, 'Input should be a floating point!'
    assert type(y_coord) == float, 'Input should be a floating point!'

    return Point(x_coord, y_coord)

#demonstrate the usage of the function
point1 = create_point_geom(0.0, 1.1)
assert type(point1) == Point, 'output point from the function should be Point variable'

try:
    #pass something else than two floats
    create_point_geom('Gimme a point!', 'Now!')
except AssertionError:
    print('Point float check works')
except Exception as e:
    raise e

def create_line_geom(points):
    '''creates a line object from a list of point objects

    Args:
        points: a list variable of two or more points

    Returns:
        LineString(points): a single Linestring variable formed
                            from the points in the input list
    '''

    #Checking that the input for parameter is a list
    assert type(points) == list, 'Input should be a list!'

    #Checking the the input contains at least two points
    assert len(points) >= 2, 'LineString object requires at least two Points!'

    #Checking the input list contains only points. I only got this to work by adding a point variable
    #inside the type() tool
    for i in points:
        if isinstance(i, Point):
            continue;
        else:
            raise AssertionError ('All list values should be Shapely Point objects!')

    #Create the LineString with the list of points
    return LineString(points)

try:
    #pass something else than a list
    create_line_geom('Gimme a line!')
except AssertionError:
    print('Line list check works')
except Exception as e:
    raise e

def create_poly_geom(coords):
    '''creates a polygon object from a list of coordinate tuples

    Args:
        coords: a list variable consisting of tuple variables of coordinates

    Returns:
        Polygon(coords): a single Polygon variable formed from the
                        coordinate pairs in the input list
    '''

    #Checking that the input for parameter is a list
    assert type(coords) == list, 'Input should be a list!'
    #Checking the the input contains at least two points
    assert len(coords) >= 3, 'Polygon object requires at least three Points!'

    #Checking all the variables are tuples. I couldn't get this to work any other way that adding a tuple
    #variable inside the type() tool.
    for i in coords:
        if isinstance(i, Tuple):
            continue;
        else:
            raise AssertionError ('All list values should be coordinate tuples!')

    #Creating the polygon with given list of tuples
    return Polygon(coords)

try:
    #pass something else than a list
    create_poly_geom('Gimme a polygon')
except AssertionError:
    print('Poly list check works')
except Exception as e:
    raise e

#Defining the function
def get_centroid(geom):
    '''returns the centroid of the given geometry object

    Args:
        geom: a geometric object (point, linestring or polygon)

    Returns:
        geom.centroid: the centroid coordinate of the input geometry object
    '''

    #Checking that the given variable is point, line or polygon
    assert type(geom) == Point or type(geom) == LineString or type(geom) == Polygon
    'Input should be a Shapely geometry!'

    #Calculating the centroid for the input
    return geom.centroid

def get_area(polygon):
    '''returns the area of the given polygon object

    Args:
        polygon: a polygon object to calculate the area for

    Returns:
        polygon.area: a calculated area for the input object
    '''

    #Check that the given variable is a polygon
    assert type(polygon) == Polygon
    'Input should be a Polygon -object!'

    #Calculate area for the given polygon
    return polygon.area

try:
    # Pass something else than a Shapely geometry
    get_area('Gimmee an area!')
except AssertionError:
    print('Area geometry check works')
except Exception as e:
    raise e

def get_length(geom):
    '''returns the length of the given linestring or polygon object

    Args:
        geom: geometric object (linestring or polygon) to calculate the length for

    Returns:
        geom.length: length of the given geometric object
    '''

    #Check that the given variable is a line or a polygon
    assert (type(geom) == LineString or type(geom) == Polygon), ('geom should be either ' + 
                                                                'LineString or Polygon!')

    #Calculate area for the given polygon
    return geom.length

try:
    #pass something else than a LineString or Polygon
    get_length(Point(1,2))
except AssertionError:
    print('Length geometry check works')
except Exception as e:
    raise e

try:
    #pass something else than a LineString or Polygon
    get_length('Gimme a length!')
except AssertionError:
    print('Length geometry check 2 works')
except Exception as e:
    raise e

# List all functions I created
functions = [create_point_geom, create_line_geom,
             create_poly_geom, get_centroid,
             get_area, get_length]

print('I created functions for doing these tasks:\n')

for function in functions:
    #Print function name and docstring:
    print('-', function.__name__ +':', function.__doc__)