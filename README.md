QuickPlotAnimatePy
==================

Purpose
-------
This simple python script is intended to quickly produce animated line plots from multiple 2D datasets.

Requirements
------------
+ Python 3.12.4
+ Pandas 2.2.2
+ matplotlib 3.9.1

A full list of required libraries and dependancies can be found in the [requirements document](requirements.txt).

When working in the same directory, these can be installed using 
`pip install -r requirements.txt`

Useage
------
To use the script, simply invoke the using the python command on the 
animate file 
`python animate.py`

The script accepts multiple different arguments which allow control over 
the appearance of the plots and how they are saved. A full list of 
arguments can be found in the help menu, using 
`python animate.py --help`

### Important Arguments
#### files
The *files* argument is required, since it specifies what datasets 
to parse and add to the generated figure. The argument is a list of file 
path, which can be provided two ways:
+ Using a space separated list of all relative file paths.
+ Using the "*" operator at the end of a directory path.
The *directory* argument can augment this behavior by adding a 
directory path to the beginning of the provided file paths.

### Plot style arguments
These arguments take space separated lists. The order of the elements 
must match the order of the files as presented to the *files* 
argument, or in the same order produced by `ls` if using the "*" 
operator. Each element must be from the list of string specifiers for 
matplotlib:
+ labels: These can be any string of your choosing.
+ colors: https://matplotlib.org/stable/gallery/color/named_colors.html
+ markers: https://matplotlib.org/stable/api/markers_api.html

### --save
This argument specifies what path to save the generated animation to 
and is passed to matplotlib's save method. If neither this nor the 
*display* argument are used, the script will terminate without 
creating any output.