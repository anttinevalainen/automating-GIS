from shapely.geometry import Point, LineString, Polygon
import pandas as pd

#raw formatting the filepath and saving the data into a variable 'data'
#using semicolons as separator and using the columns ['from_x','from_y', 'to_x', 'to_y']
fp = r'data/travelTimes_2015_Helsinki.txt'
data = pd.read_csv(fp, sep=';', usecols=['from_x','from_y', 'to_x', 'to_y'])

#Check how many rows and columns there are:
#number of rows should be 14643
print('Number of rows: ' + str(len(data)))

#number of columns should be 4
print('Number of rows: ' + str(len(data.columns)))

#form the function that works with every dataframe with equal column names
def create_points(dataframe):
    '''Reads the origin and destination coordinates from a dataframe and brings
    them together into separate lists

    Args:
        dataframe: Dataframe variable with columns corresponding the coordinates
                    of origin and destination:
                        - from_x
                        - from_y
                        - to_x
                        - to_y

    Returns:
        orig_points: List variable of all the origin points formed from the
                    from_x & from_y columns of the dataframe
        dest_points: List variable of all the destination points formed from the
                    to_x & to_y columns of the dataframe
    '''
    #Create empty lists for coordinates
    orig_points = []
    dest_points = []

    #iterate over rows in the dataframe
    for i, row in data.iterrows():

        #Add the coordinates of each row to the lists orig_points and dest_points as tuple
        #from_x and from_y to the orig_points
        #to_x and to_y to the dest_points
        orig_points.append(Point((row['from_x'], row['from_y'])))
        dest_points.append(Point((row['to_x'], row['to_y'])))

    #check the first value of both lists
    print('ORIGIN X Y:', orig_points[0].x, orig_points[0].y)
    print('DESTINATION X Y:', dest_points[0].x, dest_points[0].y)

    #assert that the length of both lists equal to dataframe length
    assert len(orig_points) == len(data), ('Number of origin points must be the same ' +
                                        'as number of rows in the original file')
    assert len(dest_points) == len(data), ('Number of destination points must be the same ' +
                                        'as number of rows in the original file')

    return orig_points, dest_points

def create_od_lines(list1, list2):
    '''Combines two lists of point objects and connects coordinates in each
    row as linestring

    Args:
        list1: A list variable consisting Point variables (Origin points)
        list2: A list variable consisting Point variables (Destination points)

    Returns:
        lines: A list variable of all the lines from the two original lists combined
                into LineString varibales
    '''

    #Creating asserts that only lists are added as input
    assert type(list1) == list, "Input can only be lists!"
    assert type(list2) == list, "Input can only be lists!"

    #Checking that all list values are tuples (both lists)
    for i in list1:
        if isinstance(i, type(Point((45.2, 22.34)))):
            continue;
        else:
            raise AssertionError ("All list1 values should be coordinate tuples!")

    for i in list2:
        if isinstance(i, type(Point((45.2, 22.34)))):
            continue;
        else:
            raise AssertionError ("All list2 values should be coordinate tuples!")

    #Create an empty list, iterate the two input lists and create linestring variable from the coordinate pairs
    #Add each LineString to the lines list. The functon returns the lines list in the end
    lines = []

    for origin, destination in zip(list1, list2):
        lines.append(LineString([origin,destination]))

    return lines

def calculate_total_distance(list3):
    '''calculates the total length of LineStrings in a single list

    Args:
        list: A list variable consisting of LineString variables

    Returns:
        total_length: Integer variable of the total length of LineStrings in the input list
    '''

    #Checking that the input is a list
    assert type(list3) == list, "Input should be a list!"

    #Checking that the input list contains only linestring objects
    for i in list3:
        assert type(i) == LineString, "List should contains only LineString objects!"

    #Iterating through the list of linestrings and calculating their total length
    #The function returns the total length in the end
    total_length = 0.0
    for i in list3:
        total_length = (total_length + i.length)
    return total_length

#run the functions
orig_points, dest_points = create_points(data)
linelist = create_od_lines(orig_points, dest_points)
total_length = calculate_total_distance(linelist)

print('Total distance of the lines is ' + str(round(total_length, 2)) + ' kilometers')