"""
Main data preparation file
"""
from rectangles import createStationRectangles

DATA_DIRECTORY = "f:\\transfer\\data\\"

print("Create rectangles for monitoring stations...")

createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations.csv",
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_rectangles.csv")

print("Done...")
