import glob
from io import StringIO
import geopandas as gpd
import pandas as pd
import mapclassify
from pyproj import CRS
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import contextily as ctx
import mplleaflet
import folium
import os
import builtins


#define function for the filefinder
def FileFinder(YKR_ID, foldername):
    ''''finds a list of travel time matrix files based on a single YKR_ID or a list of YKR_ID values
    from a specified input folder

    Args:
        YKR_ID: A string or integer value of a single YKR grid ID OR a list of integer/string values
                of YKR grid IDs
        foldername: A string value of the folder name where YKR grid data is searched from

    Returns:
        output: A list of all the YKR grid data files found for the given grid IDs
    '''



    #########ASSERTION#########
    #make sure that given ID/IDs are (a list of) integers/strings and the foldername is string

    if type(YKR_ID) == list:

        for index in YKR_ID:

            assert (type(index) == str or
                    type(index) == int), 'The variables in a given list need to be string or integer'
    else:
        assert (type(YKR_ID) == str or
                type(YKR_ID) == int), 'The given variable must be a string, integer or list'

    assert type(foldername) == str, 'The foldername needs to be a string'
    ###########################



    #if input is a single ID, turn it into a list of one value
    if type(YKR_ID) != list:
        copy = YKR_ID
        YKR_ID = []
        YKR_ID.append(copy)


    #create a list with text files from given folder and its subfolders (recursive=true)
    list = glob.glob(foldername + '/**/*.txt', recursive=True)

    #go through the folder filenames one by one and place the YKR grid IDs in a list
    filenumbers = []
    for i in list:
        split = i.split('_')
        split = split[2].split('.')
        filenumbers.append(split[0])


    #go through the given files and see which match with input YKR_ID(s)
    filenames = []
    index = 0
    for i in filenumbers:
        file = 'TravelTimes_to_' + i + '.txt'
        index = index + 1
        print('processing file', file,'... Progress: ', str(index), '/', str(len(filenumbers)))
        #go through given YKR IDs to find if they match with the file names.
        #if a match is found, the file number is removed from it's original list
        for j in YKR_ID:
            if str(j) == i:
                filename = 'TravelTimes_to_' + str(j) + '.txt'
                filenames.append(filename)
                YKR_ID.remove(j)

    if len(filenames) < 1:
        print('No files found with given YKR ID(s)')
        return None

    #collect full filepaths for the output from the list created in the first steps
    output = []
    for i in filenames:
        for j in list:
            if i in j:
                output.append(j)
                list.remove(j)
    print('FileFinder completed! Found ' + str(len(output)) + ' files with the given YKR IDs!')
    return output




def TableJoiner(matrix_txt, output_folder):
    '''creates a layer from the given text table or a list of tables by joining the file with given
    YKR grid GeoDataFrame where from_id in Matrix file corresponds to YKR_ID in the Shapefile

    Args:
        matrix_txt: A string or a list of strings that contains the data of a single YKR cell or
                    multiple cells distance values.
        output_folder: String value of a folder the output table is saved to

    Returns:
        None
        - The function saves the output table into the output folder
    '''

    fp = r'data/MetropAccess_YKR_grid_EurefFIN.shp'
    grid = gpd.read_file(fp)

    #########ASSERTION#########
    #check that the matrix_txt is a (list of) string(s)
    if type(matrix_txt) == list:
        for index in matrix_txt:
            assert type(index) == str, 'The variables in a given list need to be in string format'
    else:
        assert type(matrix_txt) == str, 'The given variable must be a string or list'

    #check that the grid variable is a GeoDataFrame
    assert isinstance(grid, gpd.GeoDataFrame), 'grid variable needs to be a geodataframe'
    #check that the output_folder variable is a string and the folder exists
    assert isinstance(output_folder, str), 'output_folder variable needs to be a string'
    assert os.path.isdir(output_folder), 'output_folder does not exits'
    ###########################



    #matrix_txt variable is a single string
    if type(matrix_txt) == str:
        #read file from filepath, use ; as separator, use specific columns, remove no-values
        data = pd.read_csv(matrix_txt, sep=';', na_values=-1)
        data = data.loc[data['walk_t'] >= 0]
        data = data.loc[data['pt_r_t'] >= 0]
        data = data.loc[data['car_r_t'] >= 0]
        #data = data.loc[data['bike_s_t'] >= 0]

        data = data.loc[data['walk_d'] >= 0]
        data = data.loc[data['car_r_d'] >= 0]
        data = data.loc[data['pt_r_d'] >= 0]
        #data = data.loc[data['bike_t'] >= 0]

        #merge data with YKR grid file
        output = grid.merge(data, left_on='YKR_ID', right_on='from_id')

        #create filepath for the joined table and save it
        split = matrix_txt.split('_')
        split = split[2].split('.')
        out_fp = 'data/' + split[0] + '.shp'
        output.to_file(out_fp)

    #matrix_txt variable is a list of strings
    if type(matrix_txt) == list:

        #for each filepath from the list of strings
        #read file, use ; as separator, use specific columns, remove no-values
        for index in matrix_txt:
            data = pd.read_csv(index, sep=';', na_values=-1)
            data = data.loc[data['walk_t'] >= 0]
            data = data.loc[data['pt_r_t'] >= 0]
            data = data.loc[data['car_r_t'] >= 0]

            #merge data with YKR grid file
            output = grid.merge(data, left_on='YKR_ID', right_on='from_id')

            #create filepath for the joined table and save it
            split = index.split('_')
            split = split[2].split('.')
            out_fp = output_folder + '/' + split[0] + '.shp'
            output.to_file(out_fp)
    print('TableJoiner done!')


def Visualizer(YKR_ID, travelmode, traveltype, maptype, output_folder):
    '''Visualizes the travel times of a single YKR_ID or a list of YKR_IDs based on travel times by
    specified travel mode. The output maps are saved in the specified folder and their filetype
    depends on the maptype chosen

    Args:
        YKR_ID: A (list of) string(s)/integer(s) of YKR cell ID
        travelmode: (String) Can be one of the following:
                        - car
                        - public transport
                        - walking
                        - biking
        traveltype: (String) Can be either:
                        - time
                        - distance
        maptype: (String) Can be either:
                        - static
                        - interactive
        output_folder: The desired folder the finished product is saved into

    Returns:
        None
            - The function saves the output table into the output folder
    '''

    fp = r'data/MetropAccess_YKR_grid_EurefFIN.shp'
    grid = gpd.read_file(fp)

    #########ASSERTION#########
    #YKR_ID = string, integer or list of strings or integers

    if type(YKR_ID) == list:
        for index in YKR_ID:
            assert (type(index) == str or
                    type(index) == int), 'The variables in a given list need to be string or integer'
    else:
        assert (type(YKR_ID) == str or
                type(YKR_ID) == int), 'The given variable must be a string, integer or list'

    #travelmode = string AND either 'car', 'public transport', 'walking' or 'biking'
    assert type(travelmode) == str, ("Travel mode needs to be in string format. " +
                                     "Choose: 'car', 'public transport', 'walking' or 'biking'")
    assert (travelmode.lower() == 'car' or
            travelmode.lower() == 'public transport' or
            travelmode.lower() == 'walking' or
            travelmode.lower() == 'biking'), ("Travel mode needs to be either " +
                                     "'car', 'public transport', 'walking' or 'biking'")

    #traveltype = single string, one of two options
    assert type(traveltype) == str, ("comparison type variable needs to be a string. " +
                                     "Choose either 'time' or 'distance'")
    assert (traveltype.lower() == 'time' or
            traveltype.lower() == 'distance'), ("comparison type needs to be either " +
                                                "'time' or 'distance'")

    #maptype needs to be a string and can either be static or interactive
    assert type(maptype) == str, ('Map type needs to be in string format. ' +
                                  'Choose static of interactive map')
    assert (maptype.lower() == 'static' or
            maptype.lower() == 'interactive'), ("Map type needs to be either " +
                                               "'static' or 'interactive'")

    #output folder = string and an existing folder
    assert type(output_folder) == str, 'output folder needs to be in string format.'
    assert os.path.isdir(output_folder), 'output_folder does not exits'

    #grid = geodataframe
    assert isinstance(grid, gpd.GeoDataFrame), 'grid variable needs to be a geodataframe'

    #this step can either be done outside the visualizer function or within it.
    #i chose to add it within the function
    Filelist = FileFinder(YKR_ID = YKR_ID, foldername = 'data')
    TableJoiner(Filelist, grid)

    #if the filelist is empty, no travel time data could be found
    assert len(Filelist) >= 1, ('Could not find travel time data from the data folder.' +
                                'Check the input formats and data folder of Filefinder function')
    ###########################



    #for each row in the filelist, read the datafile and classify the travel modes in it
    for index in Filelist:

        split = Filelist[0].split('_')
        split = split[2].split('.')
        filename = 'data/' + split[0] + '.shp'
        map_data = gpd.read_file(filename)

        #TIME as the traveltype
        #5min intervals 0-60
        if traveltype == 'time':

            #create a function to classify.  I also created a list for the bins for a neat code
            bins = [5,10,15,20,25,30,35,40,45,50,55,60]
            classifier = mapclassify.UserDefined.make(bins=bins)
            #apply function to both columns and create 2 new columns
            #at first i had trouble with this but then I noticed to apply the double square brackets
            map_data['car_r_t_cl'] = map_data[['car_r_t']].apply(classifier)
            map_data['pt_r_t_cl'] = map_data[['pt_r_t']].apply(classifier)
            map_data['walk_t_cl'] = map_data[['walk_t']].apply(classifier)
            #map_data['bike_s_t_cl'] = map_data[['bike_s_t']].apply(classifier)

        #DISTANCE as the traveltype
        #first intervals 0,500,3000 and then 3000 rise each step
        else:
            #create a function to classify.  I also created a list for the bins for a neat code
            bins = [500,3000,6000,9000,12000,15000,18000,21000,24000,27000,30000,33000]
            classifier = mapclassify.UserDefined.make(bins=bins)
            map_data['car_r_d_cl'] = map_data[['car_r_d']].apply(classifier)
            map_data['pt_r_d_cl'] = map_data[['pt_r_d']].apply(classifier)
            map_data['walk_d_cl'] = map_data[['walk_d']].apply(classifier)
            #map_data['bike_s_d_cl'] = map_data[['bike_d_t']].apply(classifier)


        #STATIC maps
        if maptype == 'static':

            #cefine output filename and use it when saving the file:
            if traveltype == 'time':
                output_file = (output_folder + '/' + split[0] +
                               '_accessibility_by_' + travelmode.strip() +
                               'in_minutes.png')
            else:
                output_file = (output_folder + '/' + split[0] +
                               '_accessibility_by_' + travelmode.strip() +
                               'in_meters.png')

            #create the subplot and define names for the two figures for neat code
            fig, ax = plt.subplots(figsize=(10,5))

            #plot the map

            if travelmode == 'car':
                if traveltype == 'time':
                    plot = map_data.plot(column = 'car_r_t_cl', ax=ax, cmap='RdYlBu')
                else:
                    plot = map_data.plot(column = 'car_r_d_cl', ax=ax, cmap='RdYlBu')

            if travelmode == 'public transport':
                if traveltype == 'time':
                    plot = map_data.plot(column = 'pt_r_t_cl', ax=ax, cmap='RdYlBu')
                else:
                    plot = map_data.plot(column = 'pt_r_d_cl', ax=ax, cmap='RdYlBu')

            if travelmode == 'walking':
                if traveltype == 'time':
                    plot = map_data.plot(column = 'walk_t_cl', ax=ax, cmap='RdYlBu')
                else:
                    plot = map_data.plot(column = 'walk_d_cl', ax=ax, cmap='RdYlBu')

            #if travelmode == 'biking':
                #if traveltype = 'time':
                    #plot = map_data.plot(column = 'bike_s_t_cl', ax=ax, cmap='RdYlBu')
                #else:
                    #plot = map_data.plot(column = 'bike_s_d_cl', ax=ax, cmap='RdYlBu')

            #apply titles and squeeze the layout
            ax.title.set_text(split[0] + ' accessibility by ' + travelmode)
            plt.tight_layout()
            plt.savefig(output_file)

        #INTERACTIVE maps
        if maptype == 'interactive':

            #define geoid for folium mapping
            map_data['geoid'] = map_data.index.astype(str)

            #creating interactive map
            map = folium.Map(location=[60.11, 24.56],
                             tiles = 'cartodbpositron',
                             zoom_start=10,
                             control_scale=True)

            if traveltype == 'time':
                output_file = (output_folder + '/' + split[0] +
                               '_accessibility_by_' + travelmode.strip() +
                               'in_minutes.html')
            else:
                output_file = (output_folder + '/' + split[0] +
                               '_accessibility_by_' + travelmode.strip() +
                               'in_meters.html')

            #car
            if travelmode == 'car':
                if traveltype == 'time':
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','car_r_t_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in minutes')
                                      ).add_to(map)
                else:
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','car_r_d_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in meters')
                                      ).add_to(map)
            #public transport
            if travelmode == 'public transport':
                if traveltype == 'time':
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','pt_r_t_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in minutes')
                                      .add_to(map)
                    )
                else:
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','pt_r_d_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in meters')
                                      ).add_to(map)
            #walking
            if travelmode == 'walking':
                if traveltype == 'time':
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','walk_t_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in minutes')
                                      ).add_to(map)
                else:
                    folium.Choropleth(geo_data = map_data,
                                      data = map_data,
                                      columns = ['geoid','walk_d_cl'],
                                      key_on = 'feature.id',
                                      fill_color = 'RdYlBu',
                                      line_color = 'white',
                                      line_weight = 0,
                                      legend_name = (split[0] + ' accessibility by ' +
                                                     travelmode + ' in meters')
                                      ).add_to(map)
            #biking
            #if travelmode == 'biking':
                #if traveltype == 'time':
                    #folium.Choropleth(geo_data = map_data,
                                      #data = map_data,
                                      #columns = ['geoid','bike_s_t_cl'],
                                      #key_on = 'feature.id',
                                      #fill_color = 'RdYlBu',
                                      #line_color = 'white',
                                      #line_weight = 0,
                                      #legend_name = (split[0] + ' accessibility by ' +
                                                     #travelmode + ' in minutes')
                                      #).add_to(map)
                #else:
                    #folium.Choropleth(geo_data = map_data,
                                      #data = map_data,
                                      #columns = ['geoid','bike_d_cl'],
                                      #key_on = 'feature.id',
                                      #fill_color = 'RdYlBu',
                                      #line_color = 'white',
                                      #line_weight = 0,
                                      #legend_name = (split[0] + ' accessibility by ' +
                                                     #travelmode + ' in meters')
                                      #).add_to(map)

            #save the html file
            map.save(output_file)

    print('Visualizer done! Thank you for your patience!')


#define function for the ComparisonTool
def ComparisonTool(YKR_ID, comparison, comparisontype, output_folder):
    '''Compares travel times or travel distances between two different travel modes.
    For example, compare rush hour travel times by public transport and car based on columns
    pt_r_t and car_r_t, and rush hour travel distances based on columns pt_r_d and car_r_d.

    Given comparisons need to be in a list of two travel modes. In the calculation, the first travel
    mode is always subtracted by the last one: travelmode1 - travelmode2 according to the order in which
    the travel modes were listed. The tool saves outputs as new shapefile. Accepted travel modes are the
    same ones that are found in the actual TravelTimeMatrix file (car, public transport, walking, biking).

    Args:
        YKR_ID: A (list of) string(s)/integer(s) of YKR cell ID
        comparison: A list of two different travel modes (string). The travel modes are:
                    - car
                    - public transport
                    - walking
                    - biking
                    (comparison can also be a single string of a travelmode above. In this
                    case the function produces a simple travel time matrix)
        comparisontype: (String) Can be either:
                    - time
                    - distance
        output_folder: The desired folder the finished product is saved into

    Returns:
        None
            - The function saves the output table into the output folder

    '''

    fp = r'data/MetropAccess_YKR_grid_EurefFIN.shp'
    grid = gpd.read_file(fp)

    #########ASSERTION#########

    #YKR_ID = string, integer or list of strings or integers

    if type(YKR_ID) == list:
        for index in YKR_ID:
            assert (type(index) == str or
                    type(index) == int), 'The variables in a given list need to be string or integer'
    else:
        assert (type(YKR_ID) == str or
                type(YKR_ID) == int), 'The given variable must be a string, integer or list'

    #comparison = single string or list of two strings specifying travel modes (four possible travel modes)
    assert (type(comparison) == list or
            type(comparison) == str), ("The comparison variable needs to be a list of two " +
                                       "of the four given travel modes. For example ['car', 'bike']. " +
                                       "The list items need to be in string format. For a travel time " +
                                       "map of a single travelmode, the comparison variable needs to be " +
                                       "a single string. Possible travel modes are " +
                                       "'car', 'biking', 'public transport' and 'walking'")

    if type(comparison) == str:
        assert (comparison == 'car' or
         comparison == 'public transport' or
         comparison == 'walking' or
         comparison == 'biking'), ("Travel mode needs to be either " +
                                   "'car', 'public transpor', 'walking' or 'biking'")

    if type(comparison) == list:
        assert len(comparison) == 2, 'The comparison list can only contain two variables'

        assert comparison[0] != comparison[1], 'The variables in comparison list must be different travel types'

        for travelmode in comparison:
            assert (travelmode == 'car' or
             travelmode == 'public transport' or
             travelmode == 'walking' or
             travelmode == 'biking'), ("Travel mode needs to be either " +
                                       "'car', 'public transport', 'walking' or 'biking'")

    #comparisontype = single string of two options
    assert type(comparisontype) == str, ("comparison type variable needs to be a string. " +
                                         "Choose either 'time' or 'distance'")
    assert (comparisontype == 'time' or
            comparisontype == 'distance'), "comparison type needs to be either 'time' or 'distance'"

    #grid = geodataframe
    assert isinstance(grid, gpd.GeoDataFrame), 'grid variable needs to be a geodataframe'

    #output folder = string
    assert type(output_folder) == str, 'output folder needs to be in string format.'
    assert os.path.isdir(output_folder), 'output_folder does not exits'

    #This step can either be done outside the visualizer function or within it. I chose to add it within the function
    Filelist = FileFinder(YKR_ID = YKR_ID, foldername = 'data')
    TableJoiner(Filelist, grid)

    #if the filelist is empty, no travel time data could be found
    assert len(Filelist) >= 1, ("Could not find travel time data from the data folder. " +
                                "Check the input formats and data folder of Filefinder function")
    ###########################




    #If the given IDs are a list of IDs
    for index in Filelist:
        split = Filelist[0].split('_')
        split = split[2].split('.')
        filename = 'data/' + split[0] + '.shp'
        map_data = gpd.read_file(filename)

        fig, ax = plt.subplots(figsize=(10,5))

        walk_time = map_data['walk_t']
        walk_distance = map_data['walk_d']

        car_time = map_data['car_r_t']
        car_distance = map_data['car_r_d']

        pt_time = map_data['pt_r_t']
        pt_distance = map_data['pt_r_d']

        """bike_time = map_data['bike_s_t']
        bike_distance = map_data['bike_d']"""

        if type(comparison) == str or len(comparison) == 1:
            Visualizer(YKR_ID = YKR_ID, travelmode = comparison, traveltype = comparisontype, maptype = 'static', output_folder = output_folder, grid = grid)


        #make the conditional statements to define the comparisons
        else:
            map_data['result'] = ""

            if comparison[0] == 'walk':
                if comparison[1] == 'car':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[walk_time] - map_data[car_time]
                    else:
                        map_data['result'] = map_data[walk_distance] - map_data[car_distance]


                elif comparison[1] == 'public transport':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[walk_time] - map_data[pt_time]
                    else:
                        map_data['result'] = map_data[walk_distance] - map_data[pt_distance]

                """else:
                    if comparisontype == 'time':
                        map_data['result'] = map_data[walk_time] - map_data[bike_time]
                    else:
                        map_data['result'] = map_data[walk_distance] - map_data[bike_distance]"""

            elif comparison[0] == 'car':
                if comparison[1] == 'walk':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[car_time] - map_data[walk_time]
                    else:
                        map_data['result'] = map_data[car_distance] - map_data[walk_distance]


                elif comparison[1] == 'public transport':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[car_time] - map_data[pt_time]
                    else:
                        map_data['result'] = map_data[car_distance] - map_data[pt_distance]

                """else:
                    if comparisontype == 'time':
                        map_data['result'] = map_data[car_time] - map_data[bike_time]
                    else:
                        map_data['result'] = map_data[car_distance] - map_data[bike_distance]"""

            else:
                if comparison[1] == 'walk':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[pt_time] - map_data[walk_time]
                    else:
                        map_data['result'] = map_data[pt_distance] - map_data[walk_distance]


                elif comparison[1] == 'car':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[pt_time] - map_data[car_time]
                    else:
                        map_data['result'] = map_data[pt_distance] - map_data[car_distance]

                '''else:
                    if comparisontype == 'time':
                        map_data['result'] = map_data[car_time] - map_data[bike_time]
                    else:
                        map_data['result'] = map_data[car_distance] - map_data[bike_distance]'''

            """else:
                if comparison[1] == 'walk':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[bike_time] - map_data[walk_time]
                    else:
                        map_data['result'] = map_data[bike_distance] - map_data[walk_distance]


                elif comparison[1] == 'public transport':
                    if comparisontype == 'time':
                        map_data['result'] = map_data[bike_time] - map_data[pt_time]
                    else:
                        map_data['result'] = map_data[bike_distance] - map_data[pt_distance]

                else:
                    if comparisontype == 'time':
                        map_data['result'] = map_data[bike_time] - map_data[car_time]
                    else:
                        map_data['result'] = map_data[bike_distance] - map_data[car_distance]"""

            #plot the data and save the figure
            plot = map_data.plot(column = 'result', ax=ax, cmap='RdYlBu')
            filepath = ('Accessibility_' + split[0] + '_' + comparison[0].strip() +
                        '_vs_' + comparison[1].strip() + comparisontype + '.png')
            plt.savefig(filepath)
    print('Comparisontool finished!')
