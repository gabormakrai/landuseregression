"""
Main data preparation file
"""
from rectangles import createStationRectangles
from traffic import createTrafficGISFile, createRectangleTraffic,\
    addTimestampToTraffic
from topobuildings import generateAllBuildingGisInformation,\
    generateRectangleBuildings, multiplyBuildingData
from yorktime import createTimeFile
from join import joinFiles
from Timestamp import generateDatesStringForYear, generateTimestamps
from osmpolygons import getRectangleOSMPolygons, multiplyLanduseData,\
    loadPolygons, saveDownAllCategory, saveAllPolygonsGis, multiplyLanduseData2
from airquality import processAirQualityFiles, writeOutHourlyData,\
    processAurnFiles
from atc import processAtcData, general_stats_about_london_atc
from osmgrabber import downloadOsmData, getPolygonsFromOSM,\
    getPolygonsWithoutHistoryFromOSM, getPolygonCategoriesFromOSM
from weather import downloadWUDataForStations, processWUData,\
    processWUDataLocation

DATA_DIRECTORY = "/home/makrai/data/london/"
 
print("Create rectangles for monitoring stations...")
      
createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_rectangles.csv",
    "\t")
      
print("Done...")
  
print("Download osm data for the London area...")
  
downloadOsmData(-1.05, 0.75, 51.05, 51.75, DATA_DIRECTORY + "osm/downloaded/", "\t")
  
print("Done...")
  
print("Parse osm data for polygons...")
  
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/polygons.csv", 
    "\t")
  
getPolygonCategoriesFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/categories_all.csv", 
    "\t")
  
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/poly_building.csv",
    "\t",
    ("building"))
   
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/poly_leisure.csv", 
    "\t",
    ("leisure"))
   
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/poly_natural.csv", 
    "\t",
    ("natural"))
   
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/poly_landuse.csv", 
    "\t",
    ("landuse"))
  
polygons = loadPolygons(DATA_DIRECTORY + "osm/poly_building.csv", "\t")
saveAllPolygonsGis(polygons, DATA_DIRECTORY + "gis/poly_building.csv", "\t")
polygons = loadPolygons(DATA_DIRECTORY + "osm/poly_landuse.csv", "\t")
saveAllPolygonsGis(polygons, DATA_DIRECTORY + "gis/poly_landuse.csv", "\t")
polygons = loadPolygons(DATA_DIRECTORY + "osm/poly_leisure.csv", "\t")
saveAllPolygonsGis(polygons, DATA_DIRECTORY + "gis/poly_leisure.csv", "\t")
polygons = loadPolygons(DATA_DIRECTORY + "osm/poly_natural.csv", "\t")
saveAllPolygonsGis(polygons, DATA_DIRECTORY + "gis/poly_natural.csv", "\t")
 
print("Done")
  
  
getRectangleOSMPolygons(
    DATA_DIRECTORY + "osm/poly_building.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    "building",
    True,
    DATA_DIRECTORY + "preprocessed_hour/osm_building.csv",
    DATA_DIRECTORY + "gis/osm_building.csv",                
    "\t")
  
getRectangleOSMPolygons(
    DATA_DIRECTORY + "osm/poly_natural.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    "building",
    False,
    DATA_DIRECTORY + "preprocessed_hour/osm_natural.csv",
    DATA_DIRECTORY + "gis/osm_natural.csv",                
    "\t")
  
getRectangleOSMPolygons(
    DATA_DIRECTORY + "osm/poly_landuse.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    "building",
    False,
    DATA_DIRECTORY + "preprocessed_hour/osm_landuse.csv",
    DATA_DIRECTORY + "gis/osm_landuse.csv",                
    "\t")
  
getRectangleOSMPolygons(
    DATA_DIRECTORY + "osm/poly_leisure.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    "building",
    False,
    DATA_DIRECTORY + "preprocessed_hour/osm_leisure.csv",
    DATA_DIRECTORY + "gis/osm_leisure.csv",                
    "\t")
 
multiplyLanduseData2(
    DATA_DIRECTORY + "preprocessed_hour/osm_building.csv",
    generateTimestamps(2015),
    DATA_DIRECTORY + "preprocessed_hour/osm_building_2015.csv",
    "\t")
multiplyLanduseData2(
    DATA_DIRECTORY + "preprocessed_hour/osm_leisure.csv",
    generateTimestamps(2015),
    DATA_DIRECTORY + "preprocessed_hour/osm_leisure_2015.csv",
    "\t")
multiplyLanduseData2(
    DATA_DIRECTORY + "preprocessed_hour/osm_landuse.csv",
    generateTimestamps(2015),
    DATA_DIRECTORY + "preprocessed_hour/osm_landuse_2015.csv",
    "\t")
multiplyLanduseData2(
    DATA_DIRECTORY + "preprocessed_hour/osm_natural.csv",
    generateTimestamps(2015),
    DATA_DIRECTORY + "preprocessed_hour/osm_natural_2015.csv",
    "\t")
        
print("Generating ATC stats")

general_stats_about_london_atc(DATA_DIRECTORY + "atc/atc_2015.csv", "\t")

print("Done...")

print("Creating time related dataset...")
     
createTimeFile(
    generateTimestamps(2015), 
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    DATA_DIRECTORY + "preprocessed_hour/time.csv",
    "\t",
    yorkSpecific=False)
       
print("Done...")
   
   
print("Creating time related dataset (binned)...")
    
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/yorktime2_" + str(year) +".csv",
        "\t",
        binned=True)
      
print("Done...")
  
   
print("Processing data air quality files...")
     
print("Loading data air quality data...")
data = processAurnFiles(
    [2015], 
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv", 
    DATA_DIRECTORY + "aq/", 
    "\t")
     
print("Done...")
     
print("Writing out hourly averages...")
     
writeOutHourlyData(
    data,
    DATA_DIRECTORY + "preprocessed_hour/airquality.csv", 
    "\t")
     
print("Done...")
         
print("Done...")
  
  
print("Download weather data from WUnderground...")
    
downloadWUDataForStations(
    ["713a5d5ba669dab2", "a4083adf99e6ff74", "8fd2210e7d8dfeb7", "0ec4fab9d96c8700","299502676d08a88c","024dbed73b2dd7f5", "94d1c774e38510ad", "456ffeef87394525", "3c808a121d2d1512"],
    DATA_DIRECTORY + "stations/stations.csv", 
    generateDatesStringForYear(2015), 
    DATA_DIRECTORY + "weather/wu/", 
    "\t")
      
# print("Done...")
#     
   
print("Processing WU weather data...")
processWUDataLocation(
    DATA_DIRECTORY + "weather/wu/", 
    DATA_DIRECTORY + "preprocessed_hour/weather" + ".csv", 
    "\t")
print("Done...")
   
print("Processing WU weather data (binned)...")
        
for year in years: 
    processWUData(
        generateTimestamps(year),
        DATA_DIRECTORY + "weather/wu/", 
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/weather2_" + str(year) + ".csv", 
        "\t",
        fileList = None,
        binned=True)
         
print("Done...")
  
print("Processing ATC data...")
  
for year in years:
    processAtcData(
        year,
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv", 
        DATA_DIRECTORY + "atc/",
        DATA_DIRECTORY + "preprocessed_hour/atc_" + str(year) + ".csv", 
        "\t")
  
print("Done...")
 
   
print("Joining preprocessed files...")
           
filesToJoin = [
#     DATA_DIRECTORY + "preprocessed_hour/traffic_" + str(year) + ".csv",
#     DATA_DIRECTORY + "preprocessed_hour/topo_timestamp_" + str(year) + ".csv",
#     DATA_DIRECTORY + "preprocessed_hour/osmlanduse_" + str(year) + ".csv",
    DATA_DIRECTORY + "preprocessed_hour/airquality.csv",
    DATA_DIRECTORY + "preprocessed_hour/weather.csv",
    DATA_DIRECTORY + "preprocessed_hour/time.csv"]
                
joinFiles(
    filesToJoin,
    DATA_DIRECTORY + "data_hour_2015.csv",
    False,
    "\t")
                
print("Done...")
     
