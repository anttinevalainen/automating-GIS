import glob
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os


#read file from filepath
fp = r'data/MetropAccess_YKR_grid_EurefFIN.shp'
grid = gpd.read_file(fp)
#glob the data-folder
filepaths = glob.glob('data/*.txt')

#action for each txt file in the data folder
for file in filepaths:
    #read file into a dataframe called data, use ; as separator and use specific columns only
    data = pd.read_csv(file, sep=';', usecols=['from_id', 'pt_r_t'])
    #remove nodata-values (-1)
    data = data.loc[data['pt_r_t'] >= 0]

    #get only the shopping center name from the filepath and rename the pt_r_t column for each center
    split = file.split('_')
    sc_name = split[-1][:-4]
    filepath = 'pt_r_t_' + sc_name

    #rename the columns by the filepath above
    data = data.rename(columns = {'pt_r_t': filepath, 'from_id': 'YKR_ID'})
    #merge the data from each center into the YKR grid
    grid = grid.merge(data, left_on='YKR_ID', right_on='YKR_ID')


#############ASSERTIONS###################
# Check that there are correct number of columns
assert len(grid.columns) >= 9, "There are some columns missing from the grid."
##########################################



# Create a new column for minimum travel time values
value_columns = ['pt_r_t_Jumbo', 'pt_r_t_Dixi',
                 'pt_r_t_Myyrmanni', 'pt_r_t_Itis',
                 'pt_r_t_Forum', 'pt_r_t_IsoOmena',
                 'pt_r_t_Ruoholahti']
grid['min_t'] = None

# Iterate over rows of the dataframe
for index, row in grid.iterrows():
    #define min value for the row with the list of value columns
    min_value = row[value_columns].min()
    #add the min value of each row to the min_t column
    grid['min_t'].loc[index] = min_value

# Create a new column for the closest shopping center id values
grid['dominant_service'] = None

# Iterate over rows of the dataframe
for index, row in grid.iterrows():
    #define the closest column for each grid with the list of value columns
    closest = row[value_columns].astype(float).idxmin()
    #add the closest service of each row to the dominant service column
    grid['dominant_service'].loc[index] = closest


#VISUALISATION

#define output filename
output_fig = r"data/closest_shopping_centers.png"

#create a subplot and define names for the two figures for neat code
fig, axes = plt.subplots(1, 2, figsize=(10,5))
ax1 = axes[0]
ax2 = axes[1]

#plot the maps by the two classified columns, apply color scheme
domplot = grid.plot(column = 'dominant_service', ax=ax1, cmap='RdYlBu')
timeplot = grid.plot(column = 'min_t', ax=ax2, cmap='RdYlBu')

#apply titles and squeeze the layout
ax1.title.set_text('Dominance areas of shopping centers')
ax2.title.set_text('Travel times to nearest shopping center')
plt.tight_layout()

plt.savefig(output_fig)

#################ASSERTIONS#####################
assert os.path.isfile(output_fig), 'file does not exists in the filepath!'
################################################