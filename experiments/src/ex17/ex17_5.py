"""
Script to load Air Quality data for many years
and create graphs based on averages...
"""

from airquality import processAirQualityFiles
import numpy as np
import matplotlib.pyplot as plt
from rectangles import loadRectangles

DATA_DIRECTORY = "/media/sf_lur/data/"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex17/"

rectangleFile = DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv" 

years = [2012,2013,2014,2015] 
years = [2013]

print("Loading AQ data...")

data = processAirQualityFiles(
    "no2", 
    years, 
    rectangleFile, 
    DATA_DIRECTORY + "aq/",
    "\t"
    )

# generate statistics

overall = {}
stationHistogram = {}
for key in data:
    stationHistogram[key] = {}

for stationId in data:
    for timestamp in data[stationId]:
        bucket = int(data[stationId][timestamp])
        if bucket not in overall:
            overall[bucket] = 1
        else:
            overall[bucket] = overall[bucket] + 1
        if bucket not in stationHistogram[stationId]:
            stationHistogram[stationId][bucket] = 1
        else:
            stationHistogram[stationId][bucket] = stationHistogram[stationId][bucket] + 1

def doGraph(data, title, fileName):
    
    names = []
    dataToPlot = []
    for i in range(0,140):
        names.append(str(i))
        if i in data:
            dataToPlot.append(data[i])
        else:
            dataToPlot.append(0)
    
    index = np.arange(len(names))
    bar_width = 0.8
    
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.bar(index, dataToPlot, bar_width, color='b', edgecolor='none')
    
    plt.xlabel("No2 concentration level (ug/m3)")
    plt.ylabel("#observation")
    plt.title(title)
     
    plt.margins(0.04, 0.04)
     
    plt.savefig(fileName)

doGraph(
    overall,
    "Histogram of No2 distribution in York (2013)",
    OUTPUT_DIRECTORY + "histogram2_overall.png")

rectangles = []
loadRectangles(rectangles, rectangleFile, "\t")

for rectangle in rectangles:
    
    doGraph(
        stationHistogram[rectangle.ID],
        "Histogram of No2 distribution at " + rectangle.name + " (2013)",
        OUTPUT_DIRECTORY + "histogram_" + rectangle.name.lower() + ".png")

