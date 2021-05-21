def Visualizer(YKR_ID, travelmode, traveltype, maptype, output_folder):
    import geopandas as gpd
    import os
    from FileFinder import FileFinder
    from TableJoiner import TableJoiner
    import mapclassify
    import matplotlib.pyplot as plt
    import folium
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
