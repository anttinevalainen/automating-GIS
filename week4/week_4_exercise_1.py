import geopandas as gpd
import pandas as pd
import mapclassify
import matplotlib.pyplot as plt
import os

#read in the YKR gri data
fp = r'data/MetropAccess_YKR_grid_EurefFIN.shp'
grid = gpd.read_file(fp)

#read in the travel times -file, use specific columns and remove values less than 0
fp = r'data/TravelTimes_to_5944003_Itis.txt'
data = pd.read_csv(fp, sep=';', usecols=['pt_r_t', 'car_r_t', 'from_id', 'to_id'])

#this statement is enough because the length is the same whether apply it to car_r_t column or not
data = data.loc[data['pt_r_t'] >= 0]
#i still added it for for both distance values
data = data.loc[data['car_r_t'] >= 0]


#merge data with grid['YKR_GRID'] and data['from_id']
#turning the dataframes other way around (merge data with grid) ends up with pandas dataframe, i tried
data_geo = grid.merge(data, left_on='YKR_ID', right_on='from_id',)



#################ASSERTIONS#####################
#check data type
assert type(data_geo)  == gpd.geodataframe.GeoDataFrame, 'output should be a geodataframe'

#check that the merged output has (at least) the necessary columns
required_columns = ['YKR_ID', 'pt_r_t', 'car_r_t', 'geometry']
assert all(x in data_geo.columns for x in required_columns), "Couldn't find all required columns"

#check that -1 values are not present in the columns
assert -1 not in data_geo['pt_r_t'], 'No data values should be removed from pt_r_t!'
assert -1 not in data_geo['car_r_t'], 'No data values should be removed from car_r_t!'
################################################



#create a classifier. I also created a list for the bins for a neat code
bins = [5,10,15,20,25,30,35,40,45,50,55,60]
classifier = mapclassify.UserDefined.make(bins=bins)

#apply classifier to both columns and create 2 new columns
#at first i had trouble with this but then I noticed to apply the double square brackets
data_geo['car_r_t_cl'] = data_geo[['car_r_t']].apply(classifier)
data_geo['pt_r_t_cl'] = data_geo[['pt_r_t']].apply(classifier)


# Define output filename for the figure in here and use it when saving the file:
output_fig1 = r'data/itis_accessibility.png'
#Create the subplot and define names for the two figures for neat code
fig, axes = plt.subplots(1, 2, figsize=(10,5))
ax1 = axes[0]
ax2 = axes[1]

#plot the maps by the two classified columns, apply color scheme
ptplot = data_geo.plot(column = 'pt_r_t_cl', ax=ax1, cmap='RdYlBu')
carplot = data_geo.plot(column = 'car_r_t_cl', ax=ax2, cmap='RdYlBu')

#apply titles
ax1.title.set_text('Itis travel times by PT')
ax2.title.set_text('Itis travel times by car')

#squeeze the layout and save the output
plt.tight_layout()
output_fig1 = r'data/itis_accessibility.png'
plt.savefig(output_fig1)



#################ASSERTIONS#####################
assert os.path.isfile(output_fig1), 'file does not exists in the filepath!'
################################################



#retrace the same for Myyrmanni


#read in the travel times -file, use specific columns and remove values less than 0
fp = r'data/TravelTimes_to_5902043_Myyrmanni.txt'
data = pd.read_csv(fp, sep=';', usecols=['pt_r_t', 'car_r_t', 'from_id', 'to_id'])

#this statement is enough because the length is the same whether apply it to car_r_t column or not
data = data.loc[data['pt_r_t'] >= 0]
#i still added it for for both distance values
data = data.loc[data['car_r_t'] >= 0]

#merge data with grid['YKR_GRID'] and data['from_id']
#turning the dataframes other way around (merge data with grid) ends up with pandas dataframe, i tried
data_geo = grid.merge(data, left_on='YKR_ID', right_on='from_id',)



#################ASSERTIONS#####################
#check data type
assert type(data_geo)  == gpd.geodataframe.GeoDataFrame, 'output should be a geodataframe'

#check that the merged output has (at least) the necessary columns
required_columns = ['YKR_ID', 'pt_r_t', 'car_r_t', 'geometry']
assert all(x in data_geo.columns for x in required_columns), "Couldn't find all required columns"

#check that -1 values are not present in the columns
assert -1 not in data_geo['pt_r_t'], 'No-data -values should be removed from pt_r_t!'
assert -1 not in data_geo['car_r_t'], 'No-data -values should be removed from car_r_t!'
################################################



#create a classifier. I also created a list for the bins for a neat code
bins = [5,10,15,20,25,30,35,40,45,50,55,60]
classifier = mapclassify.UserDefined.make(bins=bins)

#apply classifier to both columns and create 2 new columns
#at first i had trouble with this but then I noticed to apply the double square brackets
data_geo['car_r_t_cl'] = data_geo[['car_r_t']].apply(classifier)
data_geo['pt_r_t_cl'] = data_geo[['pt_r_t']].apply(classifier)


# Define output filename for the figure in here and use it when saving the file:
output_fig1 = r'data/myyrmanni_accessibility.png'
#Create the subplot and define names for the two figures for neat code
fig, axes = plt.subplots(1, 2, figsize=(10,5))
ax1 = axes[0]
ax2 = axes[1]

#plot the maps by the two classified columns, apply color scheme
ptplot = data_geo.plot(column = 'pt_r_t_cl', ax=ax1, cmap='RdYlBu')
carplot = data_geo.plot(column = 'car_r_t_cl', ax=ax2, cmap='RdYlBu')

#apply titles
ax1.title.set_text('Myyrmanni travel times by PT')
ax2.title.set_text('Myyrmanni travel times by car')

#squeeze the layout and save the output
plt.tight_layout()
output_fig1 = r'data/myyrmanni_accessibility.png'
plt.savefig(output_fig1)



#################ASSERTIONS#####################
assert os.path.isfile(output_fig1), 'file does not exists in the filepath!'
################################################



#creating the subplot with four spots, i also renamed the axes ax ax1-ax4
fig, axes = plt.subplots(2, 2, figsize=(10,10))
ax1 = axes[0][0]
ax2 = axes[0][1]
ax3 = axes[1][0]
ax4 = axes[1][1]

#create list of the two filenames.
list_of_sc = ['data/TravelTimes_to_5902043_Myyrmanni.txt', 'data/TravelTimes_to_5944003_Itis.txt']
#for-loop for files in the list
for file in list_of_sc:
    fp = file
    data = pd.read_csv(fp, sep=';', usecols=['pt_r_t', 'car_r_t', 'from_id', 'to_id'])
    data = data.loc[data['pt_r_t'] >= 0]
    data = data.loc[data['car_r_t'] >= 0]
    data_geo = grid.merge(data, left_on='YKR_ID', right_on='from_id',)

    bins = [5,10,15,20,25,30,35,40,45,50,55,60]
    classifier = mapclassify.UserDefined.make(bins=bins)
    data_geo['car_r_t_cl'] = data_geo[['car_r_t']].apply(classifier)
    data_geo['pt_r_t_cl'] = data_geo[['pt_r_t']].apply(classifier)

    #i ended up using conditional statements to save the plots to their places
    if file == 'data/TravelTimes_to_5902043_Myyrmanni.txt':

        ptplot = data_geo.plot(column = 'pt_r_t_cl', ax=ax1, cmap='RdYlBu')
        carplot = data_geo.plot(column = 'car_r_t_cl', ax=ax2, cmap='RdYlBu')

        ax1.title.set_text('Myyrmanni travel times by PT')
        ax2.title.set_text('Myyrmanni travel times by car')
    else:
        ptplot = data_geo.plot(column = 'pt_r_t_cl', ax=ax3, cmap='RdYlBu')
        carplot = data_geo.plot(column = 'car_r_t_cl', ax=ax4, cmap='RdYlBu')

        ax3.title.set_text('Itis travel times by PT')
        ax4.title.set_text('Itis travel times by car')

#save the output to data folder
output_fig = r'data/shopping_center_accessibility.png'
plt.savefig(output_fig)

#################ASSERTIONS#####################
assert os.path.isfile(output_fig), 'file does not exists in the filepath!'
################################################



