# Grading 

- Final assignment: 3.6/5
- Exercises, period 1: 5/5
- Exercises, period 2: 5/5
- Course grade: **5/5**

# Feedback for the final assignment

**fina-assignment-anttinevalainen:**

Most of the tools work nicely for different inputs as instructed. Comparison tool does not work, but probably is not far from working. Functions are used, but they are rather long (makes the code more difficult to debug). There is room to shorten the code by writing reduntand parts as functions. Version control (regular commits) might have helped with managing the project better - it now looks like everything was pushed to github at the last minute ;) All in all good job with the whole course! 

## Points:
- Major analysis steps: 25/40
- Overall documentation: 8/10
- Extra points: 
- Total: 36

Please find detailed feedback below. Suggestions for improvement are marked as **bold**.

### Overall documentation and structure: 

- Readme contains relevant information and link to files. 
- Files are clearly organized and named and internal links work. 
- Docstrings and adequate amount of inline comments are in place. It is, for example, possible to call `Help(function_name)` and get relevant info.
- The usage of the tool is a bit unclear. **A notebook or a script file that puts together all the analysis steps would have been nice** (for example, it could call scripts from separate script file)
- **Now some of the notebooks are formatted like script files** (for example, TableJoiner.ipynb with the docstring). This is not an error as such, but reduces readability.
- Seems that this project was pushed all at once to github (?). **Version control (regular commits) could have made it easier to manage the project.**
- **Now some of the code are repeated in several places** (redundancy)
- **Pay attention to the structure of your notebooks / script files; Always import modules at the top of the script / notebook** (not consistent now)
- **Separate folder for output maps would have been nice, so that they are easy to find** (and /or the tools /scripts could provide related documentation about where to find the outputs)

### Tools (data acquisition and analysis) 

- File finder works, also with false input :). 
    - To make it shorter (and more efficient), **could have used the glob and os modules more efficiently** (construct filename and check if it exists in stead of searching through the whole list of potential files)
- Also other tools work nicely, until the comparison tool which is probably not far from working. There are at least some issues with accessing data from dataframes in the process.
- Now that the code blocks and functions are so long, the code is a bit difficult to debug. 


### Visualization 

- Good! Plotting both static and interactive maps work :)


