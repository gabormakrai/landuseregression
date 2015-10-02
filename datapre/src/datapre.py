"""
Main data preparation file
"""
from rectangles import createStationRectangles
from traffic import createTrafficGISFile, createRectangleTraffic
from osmbuildings import getBuildingsFromOSM
from topobuildings import generateAllBuildingGisInformation,\
    generateRectangleBuildings
from osmlanduse import getLandusesFromOSM

DATA_DIRECTORY = "f:\\transfer\\data\\"

print("Create rectangles for monitoring stations...")

createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations.csv",
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_rectangles.csv",
    "\t")

print("Done...")

print("Creating traffic gis information file...")

createTrafficGISFile(
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "gis/traffic.csv",
    "\t")

print("Done...")

print("Processing traffic information for station rectangles...")

createRectangleTraffic(
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "output.csv",
    DATA_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t")

print("Done...")
   
print("Processing raw osm data for buildings...")

getBuildingsFromOSM(
    DATA_DIRECTORY + "osm/downloaded/",
    DATA_DIRECTORY + "gis/osm_buildings.csv",
    "\t")

print("Done...")

print("Processing OS Mastermap Topo layer for buildings...")

generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/york_buildings_lur.csv",
    DATA_DIRECTORY + "gis/topo_buildings.csv",
    "\t")

print("Done...")

print("Processing OS Mastermap Topo layer for buildings for rectangles...")

generateRectangleBuildings(
    DATA_DIRECTORY + "topo/york_buildings_lur.csv",
    DATA_DIRECTORY + "stations/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_buildings.csv",
    DATA_DIRECTORY + "topo/station_buildings.csv",
    "\t")
            
print("Done...")

print("Processing raw osm data for landuses...")

getLandusesFromOSM(
    DATA_DIRECTORY + "osm/downloaded/",
    DATA_DIRECTORY + "gis/osm_landuse.csv",
    "\t")

print("Done...")
