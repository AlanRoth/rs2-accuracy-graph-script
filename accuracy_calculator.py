import os
import math
import random
from decimal import Decimal
import matplotlib.pyplot as plt

### README
# This helper script was made for the The Objective RS2 Weapon Statistics Guide.
# https://steamcommunity.com/sharedfiles/filedetails/?id=2525937833
#
# The script is using calculations pulled straight out of the game files, the values from this script are objective and are values that the game uses.
#
###

### Parameters ###
# The location of the data file, you don't need to change this unless you want to use your own data.
weapon_values_file = "weaponspread.txt" 

# Set to True if you want to calculate MOA using random numbers, which is the way it is calculated when in debug mode in the game.
use_random_moa=False 

# Set to True if you want to print the toString for every gun read from file.
print_to_console=False 

# This will save the graphs to the output folder.
save_to_file=True

# Set to True if you want the graphs to have a transparent background
save_as_transparent=False

# Show MOA Histogram
moa_histogram=True

# Show deviation Scattergraphs
deviation_graphs=True

# The number of shots to 'simulate' when making the deviation scattergraph.
number_of_shots=120

# Set to true to include alt values, these seem iffy.
include_alt=True

### Do not change below unless you know what to do ###
plt.style.use('default')

cwd = os.getcwd()
output_path = cwd + "\output\\"
data_path = cwd + "\data\\"

#Check if output folder exists, if not, create it.
if not os.path.isdir(output_path):
    os.mkdir(output_path) 

### Constants ###
#Worst case RandY value
RANDY = -0.5
#Worst case RandZ value
RANDZ = -0.43301270189

### Utility & Helper Functions ###

def getFrand():
    return random.uniform(0,1)

def getYrand():
    return getFrand() - 0.5
    
def getZrand():
    randY=getYrand()
    return math.sqrt(0.50 - (randY*randY)) * (getFrand() - 0.50)

def tokenizeData(line):
    return line.split(',')

def toString(gun_data):
    gun_name = gun_data[0]
    spread = float(gun_data[1])
    spread_alt = float(gun_data[2])
    spread_multiplier = float(gun_data[3])

    moa = getMOA(spread, spread_multiplier)
    moa_alt = getMOA(spread_alt, spread_multiplier)
    absolute_deviation = getAbsoluteDeviation(spread, spread_multiplier)
    return "Name: " + gun_data[0] + " MOA: " + str(moa) + " MOA_alt: " + str(moa_alt) + " Deviation: " + str(absolute_deviation)

### Calculation Functions ###

def getMOA(spread, spread_multiplier):
    current_spread=spread if spread_multiplier == 0 else float(spread*spread_multiplier)

    #Debug menu returns moa using random Y and Z values.
    if use_random_moa:
        randY=getYrand()
        randZ=getZrand()
        moa = (math.sqrt((((randY* randY) *current_spread) *current_spread) + (((randZ * randZ)* current_spread) * current_spread)) * 4572* 2) / 2.540
        return moa

    #MOA Calculation used by the Devs, worst case
    moa = (math.sqrt((((RANDY* RANDY) *current_spread) *current_spread) + (((RANDZ * RANDZ)* current_spread) * current_spread)) * 4572* 2) / 2.540
    
    #Returns average MOA
    return moa/2

def getMoaFromData(gun_data):
    return getMOA(float(gun_data[1]), float(gun_data[3]))

def getDeviationAxis(spread, spread_multiplier):
    randY = getYrand()
    randZ = getZrand()
    
    current_spread=spread if spread_multiplier == 0 else float(spread*spread_multiplier)
    
    return [randZ * current_spread, randY * current_spread]

def getAbsoluteDeviation(spread, spread_multiplier):
    axis=getDeviationAxis(spread, spread_multiplier)
    return axis[0] + axis[1]

### Plotting Functions ###

def plotHist(values):
    for value in values:
        plt.bar(value[0], value[1], width=1)
        plt.xticks(rotation=90)
        plt.tight_layout()
    
    if save_to_file:
        plt.savefig(str(output_path + "MOA_bar_chart"), transparent=save_as_transparent)
        plt.close()
    else:
        plt.show()

def plotDeviation(gun_data):
    gun_name = gun_data[0]
    spread = float(gun_data[1])
    spread_alt = float(gun_data[2])
    spread_multiplier = float(gun_data[3])

    #Check if alt spread is different or equal to 0
    calculate_alt_spread = spread_alt != spread and spread_alt != 0 and include_alt

    plt.xlim(-0.008, 0.008)
    plt.ylim(-0.008, 0.008)
    plt.title(gun_name)
    
    spread_plot=[]
    spread_alt_plot=[]
    for shot in range(number_of_shots):
        simulated_shot=getDeviationAxis(spread, spread_multiplier)
        spread_plot.append((simulated_shot[0], simulated_shot[1]))
        
        if calculate_alt_spread:
            simulated_alt_shot=getDeviationAxis(spread_alt, spread_multiplier)
            spread_alt_plot.append((simulated_alt_shot[0], simulated_alt_shot[1]))

    plt.scatter([x[0] for x in spread_plot], [y[1] for y in spread_plot], c='b')

    if calculate_alt_spread:
        plt.scatter([x[0] for x in spread_alt_plot], [y[1] for y in spread_alt_plot], c='r')
    
    if save_to_file:
        plt.savefig(str(output_path + gun_name), transparent=save_as_transparent)
        plt.close()
    else: 
        plt.show()

### Entry ###

#Read the data from the file
with open(data_path + weapon_values_file) as file:
    lines = file.read().splitlines()

moa_values={}
#Plot values for each data point
for line in lines:
    gun_data = tokenizeData(line)
    if deviation_graphs:
        plotDeviation(gun_data)

    if print_to_console:
        print(toString(gun_data))

    if moa_histogram:
        moa_values[gun_data[0]] = float(getMoaFromData(gun_data))
        moa_values_sorted=sorted(moa_values.items(), key=lambda x: x[1], reverse=True)

if moa_histogram:
    plotHist(moa_values_sorted)


