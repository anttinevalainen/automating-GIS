# Final Assignment

## Accesviz

The assignment I did is called Accesviz, where the point is to easily see the travel times to YKR grids with different methods and also helps see the differences between travel methods

### Input data:

The point is to use the travel time matrix data, which is too large dataset for my computer so i ended up making the code with the data I had from previous exercises from the course. The data worked well enough for the needs but it lacked the times and distances for biking. I added codes for biking as well with markdown text into the code. I also used the YKR grid data of Helsinki, with which the travel time data can be combined using the `Tablejoiner` function I created.

### Analysis steps:

- I started with the [FileFinder](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/FileFinder.py), which is used with all the other codes as well. The `Filefinder` -function helps find files of a specific grid in the YKR dataset among the user's files. Next step was to combine the found data with the YKR grids, for which is done with the [TableJoiner](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/TableJoiner.py) -function I also created. I'm also using the [TableJoiner](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/TableJoiner.py) in the next functions.

- The [Visualizer](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/Visualizer.py) function plots the given YKR grid with the given travel method and travel type. The function also works with multiple YKR grids and is able to produce an interactive map or a static map. The interactive map is saved as `.html` -file and the static map is saved as a `.png` -file

- [ComparisonTool](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/ComparisonTool.py) -function uses the travel time matrix to compare different travel methods with each other.

### Results:

- [.py -file with all the functions](https://github.com/anttinevalainen/automating-GIS/tree/main/final_assignment)

- [FileFinder](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/FileFinder.py)
- [TableJoiner](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/TableJoiner.py)
- [Visualizer](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/Visualizer.py)
- [ComparisonTool](https://github.com/anttinevalainen/automating-GIS/blob/main/final_assignment/ComparisonTool.py)
