def TableJoiner(matrix_txt, output_folder):
    import pandas as pd
    import geopandas as gpd
    import os
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
