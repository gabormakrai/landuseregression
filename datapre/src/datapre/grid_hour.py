"""
Main data preparation file
"""

from Timestamp import generateTimestampsForDays, DAYS_OF_MONTH, Timestamp
from rectangles import generateGridStationRectangles, createJsonFile
from traffic import createRectangleTraffic, addTimestampToTraffic
from topobuildings import multiplyBuildingData
from osmpolygons import multiplyLanduseData
from yorktime import createTimeFile
from weather import processWUData
from join import joinFiles

DATA_DIRECTORY = "/media/sf_lur/data/"

print("Generating grid stations...")
      
generateGridStationRectangles(
    100.0, 
    54.008935099981284, 
    -1.1545045166015625, 
    53.91246116826243, 
    -1.006368896484375, 
    DATA_DIRECTORY + "pre_grid_hour/station_rectangles.csv", 
    "\t")
       
print("Done...")
  
print("Creating stations' json file...")
  
createJsonFile(
    DATA_DIRECTORY + "pre_grid_hour/station_rectangles.csv", 
    DATA_DIRECTORY + "pre_grid_hour/grid.json",
    "\t")
  
print("Done...")
 
print("Processing traffic information for station rectangles...")
     
createRectangleTraffic(
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "pre_grid_hour/station_rectangles.csv",
    DATA_DIRECTORY + "pre_grid_hour/traffic.csv",
    DATA_DIRECTORY + "gis/grid_rectangles_traffic.csv",
    "\t")
     
print("Done...")
 
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
         
    multiplyLanduseData(
        DIRECTORY + "osmpoly2015.csv", 
        timestamps, 
        DIRECTORY + "osmlanduse.csv", 
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
    DATA_DIRECTORY + "pre_grid_hour/",
    DATA_DIRECTORY + "weather/wu/",
    timestamps, 
    DATA_DIRECTORY + "grid_hour.csv")
 
for month in range(1, 13):
    for day in range(1, DAYS_OF_MONTH[month - 1] + 1):
        dayTimestamp = Timestamp().createBasedOnOther(2013, month, day, 1)
        dayTimestampKey = dayTimestamp.key[0:8]
          
        timestamps = generateTimestampsForDays(2013, month, day, day)
          
        generateDataGridHourData(
            DATA_DIRECTORY + "pre_grid_hour/",
            DATA_DIRECTORY + "weather/wu/",
            timestamps, 
            DATA_DIRECTORY + "pre_grid_hour/data/data_" + dayTimestampKey + ".csv")

