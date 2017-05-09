"""
Main data preparation file
"""

from Timestamp import generateTimestampsForDays, DAYS_OF_MONTH, Timestamp
from rectangles import generateGridStationRectangles, createJsonFile
from traffic import createRectangleTraffic, addTimestampToTraffic
from topobuildings import multiplyBuildingData, generateRectangleBuildings
from osmpolygons import multiplyLanduseData2, getRectangleOSMPolygons
from yorktime import createTimeFile
from weather import processWUData
from join import joinFiles
from osmgrabber import getPolygonsFromOSM, writeOutYearPolygons

DATA_DIRECTORY = "/home/makrai/data/york/"
WORK_DIRECTORY = "/home/makrai/data/york_grid_hour_pre/"
OUTPUT_DIRECTORY = "/home/makrai/data/york_grid_hour/"

print("Generating grid stations...")
       
generateGridStationRectangles(
    100.0, 
    54.008935099981284, 
    -1.1545045166015625, 
    53.91246116826243, 
    -1.006368896484375, 
    WORK_DIRECTORY + "station_rectangles.csv", 
    "\t")
        
print("Done...")
   
print("Creating stations' json file...")
   
createJsonFile(
    WORK_DIRECTORY + "station_rectangles.csv", 
    WORK_DIRECTORY + "grid.json",
    "\t")
   
print("Done...")
  
print("Processing traffic information for station rectangles...")
      
createRectangleTraffic(
    DATA_DIRECTORY + "traffic/traffic.csv",
    WORK_DIRECTORY + "station_rectangles.csv",
    WORK_DIRECTORY + "traffic.csv",
    WORK_DIRECTORY + "gis/grid_rectangles_traffic.csv",
    "\t")
      
print("Done...")
 
print("Generating topo builing info...")
 
generateRectangleBuildings(
    DATA_DIRECTORY + "topo/buildings_2013.csv",
    WORK_DIRECTORY + "station_rectangles.csv",
    WORK_DIRECTORY + "gis/station_buildings.csv",
    WORK_DIRECTORY + "gis/station_buildings_triangles.csv",
    WORK_DIRECTORY + "topobuildings.csv",
    100,
    "\t")
 
print("Done...")
 
print("Processing downloaded osm data...")
   
getPolygonsFromOSM(
    DATA_DIRECTORY + "osm/downloaded/",
    DATA_DIRECTORY + "osm/history/",
    WORK_DIRECTORY + "polygons.csv",
    "\t")
   
print("Done...")
   
print("Genearing polygons for each year")
    
writeOutYearPolygons(
    WORK_DIRECTORY + "polygons.csv", 
    2013, 
    WORK_DIRECTORY + "osmpoly_2013.csv", 
    WORK_DIRECTORY + "gis/osmpoly_2013.csv", 
    "\t")
    
print("Done...")
      
print("Processing osm data for landuses...")
getRectangleOSMPolygons(
    WORK_DIRECTORY + "osmpoly_2013.csv",
    WORK_DIRECTORY + "station_rectangles.csv",
    "landuse",
    False,
    WORK_DIRECTORY + "osm_landuse_2013.csv",
    WORK_DIRECTORY + "gis/stations_landuse.csv",                
    "\t")
getRectangleOSMPolygons(
    WORK_DIRECTORY + "osmpoly_2013.csv",
    WORK_DIRECTORY + "station_rectangles.csv",
    "leisure",
    False,
    WORK_DIRECTORY + "osm_leisure_2013.csv",
    WORK_DIRECTORY + "gis/stations_leisure.csv",                
    "\t")
          
print("Done")

def generateDataGridHourData(DIRECTORY, weatherDataDirectory, timestamps, outputFile):
   
    print("Add timestamps to traffic data...")
        
    addTimestampToTraffic(
        timestamps, 
        DIRECTORY + "traffic.csv", 
        DIRECTORY + "traffic_timestamps.csv", 
        "\t")
        
    print("Done...")
        
    print("Add timestamp to static topo building data...")
          
    multiplyBuildingData(
        DIRECTORY + "topobuildings.csv", 
        timestamps, 
        DIRECTORY + "topo_timestamp.csv", 
        "\t")
          
    print("Done...")
         
    print("Add timestamp to static osm poly data...")
          
    multiplyLanduseData2(
        DIRECTORY + "osm_landuse_2013.csv", 
        timestamps, 
        DIRECTORY + "osmlanduse.csv", 
        "\t")
    multiplyLanduseData2(
        DIRECTORY + "osm_leisure_2013.csv", 
        timestamps, 
        DIRECTORY + "osmleisure.csv", 
        "\t")
         
    print("Done")
             
    print("Creating time related dataset...")
         
    createTimeFile(
        timestamps, 
        DIRECTORY + "station_rectangles.csv",
        DIRECTORY + "yorktime.csv",
        "\t")
         
    print("Done...")
        
    print("Processing WU weather data...")
        
    processWUData(
        timestamps, 
        weatherDataDirectory, 
        DIRECTORY + "station_rectangles.csv",
        DIRECTORY + "weather.csv", 
        "\t")
         
    print("Done...")
       
    print("Joining preprocessed files...")
            
    filesToJoin = [
        DIRECTORY + "topo_timestamp.csv",
        DIRECTORY + "osmlanduse.csv",
        DIRECTORY + "osmleisure.csv",
        DIRECTORY + "traffic_timestamps.csv",
        DIRECTORY + "weather.csv",
        DIRECTORY + "yorktime.csv"]
            
    joinFiles(
        filesToJoin,
        outputFile,
        True,
        "\t")
            
    print("Done...")
   
print("Generate timestamps...")
  
timestamps = generateTimestampsForDays(2013, 1, 1, 1)
  
print("Done...") 
  
generateDataGridHourData(
    WORK_DIRECTORY,
    DATA_DIRECTORY + "weather/wu/",
    timestamps, 
    OUTPUT_DIRECTORY + "york_hour_grid_2013.csv")
  
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
        dayTimestamp = Timestamp().createBasedOnOther(2013, month, day, 1)
        dayTimestampKey = dayTimestamp.key[0:8]
           
        timestamps = generateTimestampsForDays(2013, month, day, day)
           
        generateDataGridHourData(
            WORK_DIRECTORY,
            DATA_DIRECTORY + "weather/wu/",
            timestamps, 
            OUTPUT_DIRECTORY + "data_" + dayTimestampKey + ".csv")

