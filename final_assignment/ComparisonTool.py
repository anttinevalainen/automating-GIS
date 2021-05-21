def ComparisonTool(YKR_ID, comparison, comparisontype, output_folder):
    import geopandas as gpd
    import os
    from FileFinder import FileFinder
    from TableJoiner import TableJoiner
    from Visualizer import Visualizer
    import matplotlib.pyplot as plt
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
