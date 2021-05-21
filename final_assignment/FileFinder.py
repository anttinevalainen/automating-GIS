

def FileFinder(YKR_ID, foldername):
    import glob
    import builtins
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

    if type(YKR_ID) == builtins.list:

        for index in YKR_ID:

            assert (type(index) == str or
                    type(index) == int), 'The variables in a given list need to be string or integer'
    else:
        assert (type(YKR_ID) == str or
                type(YKR_ID) == int), 'The given variable must be a string, integer or list'

    assert type(foldername) == str, 'The foldername needs to be a string'
    ###########################



    #if input is a single ID, turn it into a list of one value
    if type(YKR_ID) != builtins.list:
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
