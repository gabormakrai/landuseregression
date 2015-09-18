"""
Main data preparation file
"""
from rectangles import createStationRectangles
from traffic import createTrafficGISFile

DATA_DIRECTORY = "f:\\transfer\\data\\"

print("Create rectangles for monitoring stations...")

createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations.csv",
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_rectangles.csv",
    "\t")

print("Done...")

print("Processing traffic information for station rectangles...")

createTrafficGISFile(
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t")

print("Done...")
"""
inputTrafficFile = 
inputRectangleFile = 
outputFile = DATA_DIRECTORY + "preprocessed/rectangles_traffic.csv"
outputGISFile = 
"""
