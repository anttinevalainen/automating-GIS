# Final Assignment

## Accesviz

The assignment I did is called Accesviz, where the point is to easily see the travel times to YKR grids with different methods and also helps see the differences between travel methods

### Input data:

The point is to use the travel time matrix data, which is too large dataset for my computer so i ended up making the code with the data I had from previous exercises from the course. The data worked well enough for the needs but it lacked the times and distances for biking. I added codes for biking as well with markdown text into the code. I also used the YKR grid data of Helsinki, with which the travel time data can be combined using the `Tablejoiner` function I created.

### Analysis steps:

- I started with the `Filefinder`, which is used with all the other codes as well. The `Filefinder` -function helps find files of a specific grid in the YKR dataset among the user's files. Next step was to combine the found data with the YKR grids, for which is done with the `Tablejoiner` -function I also created. I'm also using the `Tablejoiner` in the next functions.

- The Visualizer function plots the given YKR grid with the given travel method and travel type. The function also works with multiple YKR grids and is able to produce an interactive map or a static map. The interactive map is saved as `.html` -file and the static map is saved as a `.png` -file

- `Comparisontool` -function uses the travel time matrix to compare different travel methods with each other.

### Results:

*All in all I think I did well with the final tasks and the course all together. The final assignment could've used some finishing touches, especially for the last function.

[Filefinder](FileFinder.py)
[TableJoiner](TableJoiner.py)
[Visualizer](Visualizer.py)
[ComparisonTool](ComparisonTool.py)

[All functions together](Final.py)