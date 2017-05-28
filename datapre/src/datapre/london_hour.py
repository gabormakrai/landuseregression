"""
Main data preparation file
"""
from rectangles import createStationRectangles
from traffic import createTrafficGISFile, createRectangleTraffic,\
    addTimestampToTraffic
from yorktime import createTimeFile
from join import joinFiles
from Timestamp import generateDatesStringForYear, generateTimestamps
from osmpolygons import getRectangleOSMPolygons, \
    loadPolygons, saveAllPolygonsGis, multiplyLanduseData2
from airquality import writeOutHourlyData, processAurnFiles
from atc import general_stats_about_london_atc,\
    process_london_atc_data
from osmgrabber import downloadOsmData, \
    getPolygonsWithoutHistoryFromOSM, getPolygonCategoriesFromOSM,\
    getHighwaysFromOSM
from weather import downloadWUDataForStations, \
    processWUDataLocation

DATA_DIRECTORY = "/home/makrai/data/london/"
WORK_DIRECTORY = "/home/makrai/data/london_hour/"
OUTPUT_DIRECTORY = "/home/makrai/data/"
 
years = [2015, 2016]

print("Create rectangles for monitoring stations...")
       
createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    WORK_DIRECTORY + "gis/station_rectangles.csv",
    "\t")
       
print("Done...")
   
print("Download osm data for the London area...")
    
downloadOsmData(-1.05, 0.75, 51.05, 51.75, DATA_DIRECTORY + "osm/downloaded/", "\t")
    
print("Done...")
    
print("Parse osm data for polygons...")
     
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_all.csv", 
    "\t")
    
getPolygonCategoriesFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_categories_all.csv", 
    "\t")
     
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_building.csv",
    "\t",
    ("building"))
      
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_leisure.csv", 
    "\t",
    ("leisure"))
      
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_natural.csv", 
    "\t",
    ("natural"))
       
getPolygonsWithoutHistoryFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "poly_landuse.csv", 
    "\t",
    ("landuse"))
     
polygons = loadPolygons(WORK_DIRECTORY + "poly_building.csv", "", "\t")
saveAllPolygonsGis(polygons, WORK_DIRECTORY + "gis/poly_building.csv", "\t")
polygons = loadPolygons(WORK_DIRECTORY + "poly_landuse.csv", "", "\t")
saveAllPolygonsGis(polygons, WORK_DIRECTORY + "gis/poly_landuse.csv", "\t")
polygons = loadPolygons(WORK_DIRECTORY + "poly_leisure.csv", "", "\t")
saveAllPolygonsGis(polygons, WORK_DIRECTORY + "gis/poly_leisure.csv", "\t")
polygons = loadPolygons(WORK_DIRECTORY + "poly_natural.csv", "", "\t")
saveAllPolygonsGis(polygons, WORK_DIRECTORY + "gis/poly_natural.csv", "\t")
    
print("Done")
      
getRectangleOSMPolygons(
    WORK_DIRECTORY + "poly_building.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    "building",
    True,
    WORK_DIRECTORY + "osm_building.csv",
    WORK_DIRECTORY + "gis/osm_building.csv",                
    "\t")
    
getRectangleOSMPolygons(
    WORK_DIRECTORY + "poly_natural.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    "natural",
    False,
    WORK_DIRECTORY + "osm_natural.csv",
    WORK_DIRECTORY + "gis/osm_natural.csv",                
    "\t")
     
getRectangleOSMPolygons(
    WORK_DIRECTORY + "poly_landuse.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    "landuse",
    False,
    WORK_DIRECTORY + "osm_landuse.csv",
    WORK_DIRECTORY + "gis/osm_landuse.csv",                
    "\t")
     
getRectangleOSMPolygons(
    WORK_DIRECTORY + "poly_leisure.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    "leisure",
    False,
    WORK_DIRECTORY + "osm_leisure.csv",
    WORK_DIRECTORY + "gis/osm_leisure.csv",                
    "\t")

for year in years:

    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_building.csv",
        generateTimestamps(year),
        WORK_DIRECTORY + "osm_building_" + str(year) + ".csv",
        "\t")
    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_leisure.csv",
        generateTimestamps(year),
        WORK_DIRECTORY + "osm_leisure_" + str(year) + ".csv",
        "\t")
    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_landuse.csv",
        generateTimestamps(year),
        WORK_DIRECTORY + "osm_landuse_" + str(year) + ".csv",
        "\t")
    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_natural.csv",
        generateTimestamps(year),
        WORK_DIRECTORY + "osm_natural_" + str(year) + ".csv",
        "\t")
         
print("Generating ATC 2015 stats")
general_stats_about_london_atc(DATA_DIRECTORY + "atc/atc_2015.csv", "\t")
print("Done...")

print("Generating ATC 2015 stats")
general_stats_about_london_atc(DATA_DIRECTORY + "atc/atc_2016.csv", "\t")
print("Done...")
 
print("Parsing atc data...")
 
for year in years:
    process_london_atc_data(
        DATA_DIRECTORY + "atc/atc_" + str(year) + ".csv", 
        DATA_DIRECTORY + "atc/atc_sites.csv", 
        WORK_DIRECTORY + "atc_" + str(year) + ".csv", 
        "\t")
  
print("Done...")
 
print("Processing osm data for static traffic data...")
getHighwaysFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    WORK_DIRECTORY + "traffic.csv", 
    WORK_DIRECTORY + "gis/traffic.csv", 
    "\t")
print("Done")
 
print("Creating traffic gis information file...")
      
createTrafficGISFile(
    WORK_DIRECTORY + "stations_rectangles.csv",
    WORK_DIRECTORY + "traffic.csv",
    WORK_DIRECTORY + "gis/traffic.csv",
    "\t")
      
print("Done...")
   
print("Processing traffic information for station rectangles...")
      
createRectangleTraffic(
    WORK_DIRECTORY + "traffic.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    WORK_DIRECTORY + "traffic_stations.csv",
    WORK_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t",
    True)
      
print("Done...")
     
print("Add timestamps to traffic data...")

for year in years:
    addTimestampToTraffic(
        generateTimestamps(year), 
        WORK_DIRECTORY + "traffic_stations.csv", 
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv", 
        "\t",
        True)
        
print("Done...")
  
print("Creating time related dataset...")
       
for year in years:
    createTimeFile(
        generateTimestamps(year), 
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "time_" + str(year) + ".csv",
        "\t",
        yorkSpecific=False)
         
print("Done...")
       
print("Processing data air quality files...")
       
print("Loading data air quality data...")

for year in years:
    data = processAurnFiles(
        [year], 
        WORK_DIRECTORY + "stations_rectangles.csv", 
        DATA_DIRECTORY + "aq/", 
        "\t")
    writeOutHourlyData(
        data,
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv", 
        "\t")
       
print("Done...")
          
print("Download weather data from WUnderground...")
      
downloadWUDataForStations(
    ["713a5d5ba669dab2", "a4083adf99e6ff74", "8fd2210e7d8dfeb7", "0ec4fab9d96c8700","299502676d08a88c","024dbed73b2dd7f5", "94d1c774e38510ad", "456ffeef87394525", "3c808a121d2d1512"],
    DATA_DIRECTORY + "stations/stations.csv", 
    generateDatesStringForYear(2015), 
    DATA_DIRECTORY + "weather/wu2015/", 
    "\t")
downloadWUDataForStations(
    ["713a5d5ba669dab2", "a4083adf99e6ff74", "8fd2210e7d8dfeb7", "0ec4fab9d96c8700","299502676d08a88c","024dbed73b2dd7f5", "94d1c774e38510ad", "456ffeef87394525", "3c808a121d2d1512"],
    DATA_DIRECTORY + "stations/stations.csv", 
    generateDatesStringForYear(2016), 
    DATA_DIRECTORY + "weather/wu2016/", 
    "\t")
        
print("Done...")
     
print("Processing WU weather data...")
 
for year in years:
    processWUDataLocation(
        DATA_DIRECTORY + "weather/wu" + str(year) + "/", 
        WORK_DIRECTORY + "weather_" + str(year) + ".csv", 
        "\t")
 
print("Done...")
     
print("Joining preprocessed files...")

for year in years:              
    filesToJoin = [
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_landuse_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_natural_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_leisure_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_building_" + str(year) + ".csv",
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv",
        WORK_DIRECTORY + "weather_" + str(year) + ".csv",
        WORK_DIRECTORY + "time_" + str(year) + ".csv"]
                       
    joinFiles(
        filesToJoin,
        OUTPUT_DIRECTORY + "london_hour_" + str(year) + ".csv",
        False,
        "\t")
                   
print("Done...")
 
print("Joining preprocessed files...")

for year in years:              
    filesToJoin = [
        WORK_DIRECTORY + "atc_" + str(year) + ".csv",
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_landuse_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_natural_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_leisure_" + str(year) + ".csv",
        WORK_DIRECTORY + "osm_building_" + str(year) + ".csv",
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv",
        WORK_DIRECTORY + "weather_" + str(year) + ".csv",
        WORK_DIRECTORY + "time_" + str(year) + ".csv"]
    joinFiles(
        filesToJoin,
        OUTPUT_DIRECTORY + "london3_hour_" + str(year) + ".csv",
        False,
        "\t")
                   
print("Done...")
