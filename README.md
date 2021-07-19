# rs2-accuracy-graph-script
A small script made for the Objective RS2 Weapon Statistics Guide, using calculations from the RS2 source code.

![](https://img.shields.io/badge/Language-Python-informational?style=flat&logo=python&logoColor=white&color=2bbc8a)
![](https://img.shields.io/badge/System-Windows-informational?style=flat&logo=windows&logoColor=white&color=2bbc8a)

# How To Run The Script
*The script was made on windows and uses windows delimiters for file paths, if you wish to run this in linux you will need to change these delimiters in the code.*

*Prerequisites*
- Python3+

The script is ready to run out of the box. If you have python installed to your PATH you will be able to run *accuracy_calculator.py* which will output the graphs to a output folder by default.

## Configuration
You will be able to change these in the source code. Default values will save graphs to the output folder.

### weapon_values_file
*Default: weaponspread.txt*
The location of the data file, you don't need to change this unless you want to use your own data. 

### use_random_moa
*Default: False*
Set to True if you want to calculate MOA using random numbers, which is the way it is calculated when in debug mode in the game.

### print_to_console
*Default: False*
Set to True if you want to print the toString for every gun read from file.

### save_to_file
*Default: True*
This will save the graphs to the output folder.

### save_as_transparent
*Default: False*
Set to True if you want the graphs to have a transparent background

### moa_histogram
*Default: True*
Show MOA Histogram

### deviation_graphs
*Default: True*
Show deviation Scattergraphs


### number_of_shots
*Default: 120*
The number of shots to 'simulate' when making the deviation scattergraph.

### include_alt
*Default: True*
Set to true to include alt values, these seem iffy.

##

