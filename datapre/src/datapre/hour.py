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
from weather import downloadWeatherDataFromWunderground, processWUData
from osmpolygons import getRectangleOSMPolygons, multiplyLanduseData
from airquality import processAirQualityFiles, writeOutHourlyData
from atc import processAtcData

DATA_DIRECTORY = "/media/sf_lur/data/"
 
years = [2012, 2013, 2014, 2015]

print("Create rectangles for monitoring stations...")
    
createStationRectangles(
    100.0, 
#    DATA_DIRECTORY + "stations/stations_withoutbootham.csv",
    DATA_DIRECTORY + "stations/stations.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    DATA_DIRECTORY + "gis/station_rectangles.csv",
    "\t")
    
print("Done...")
   
print("Creating traffic gis information file...")
   
createTrafficGISFile(
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "gis/traffic.csv",
    "\t")
   
print("Done...")
  
print("Add timestamps to traffic data...")
for year in years:
    addTimestampToTraffic(
        generateTimestamps(year), 
        DATA_DIRECTORY + "preprocessed_hour/traffic.csv", 
        DATA_DIRECTORY + "preprocessed_hour/traffic_" + str(year) + ".csv", 
        "\t")
    
print("Done...")
   
   
print("Processing traffic information for station rectangles...")
   
createRectangleTraffic(
    DATA_DIRECTORY + "traffic/traffic.csv",
    DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
    DATA_DIRECTORY + "preprocessed_hour/traffic.csv",
    DATA_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t")
   
print("Done...")
  
print("Processing OS Mastermap Topo layer for buildings...")
  
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2012.csv",
    DATA_DIRECTORY + "gis/buildings_2012.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2013.csv",
    DATA_DIRECTORY + "gis/buildings_2013.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2014.csv",
    DATA_DIRECTORY + "gis/buildings_2014.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2015.csv",
    DATA_DIRECTORY + "gis/buildings_2015.csv",
    "\t")
  
print("Done...")
   
print("Processing OS Mastermap Topo layer for buildings for station rectangles...")
for year in years:   
    generateRectangleBuildings(
        DATA_DIRECTORY + "topo/buildings_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "gis/station_buildings.csv",
        DATA_DIRECTORY + "gis/station_buildings_triangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/topo_" + str(year) + ".csv",
        100,
        "\t")
                 
print("Done...")
  
print("Add timestamp to static topo building data...")
  
for year in years: 
    multiplyBuildingData(
        DATA_DIRECTORY + "preprocessed_hour/topo_" + str(year) + ".csv", 
        generateTimestamps(year), 
        DATA_DIRECTORY + "preprocessed_hour/topo_timestamp_" + str(year) + ".csv", 
        "\t")
    
print("Done...")
 
   
print("Processing osm data for landuses...")
for year in years:
    getRectangleOSMPolygons(
        DATA_DIRECTORY + "osm/osmpoly_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/osmpoly_" + str(year) +".csv",
        DATA_DIRECTORY + "gis/stations_landuse.csv",                
        "\t")
       
print("Done")
    
print("Add timestamp to static osm poly data...")
for year in years:
    multiplyLanduseData(
        DATA_DIRECTORY + "preprocessed_hour/osmpoly_" + str(year) + ".csv", 
        generateTimestamps(year), 
        DATA_DIRECTORY + "preprocessed_hour/osmlanduse_" + str(year) + ".csv", 
        "\t")
print("Done")
       
print("Creating time related dataset...")
  
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/yorktime_" + str(year) +".csv",
        "\t")
    
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
  
for year in years:     
    print("Loading data air quality data...")
    data = processAirQualityFiles(
        "no2", 
        [year], 
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv", 
        DATA_DIRECTORY + "aq/", 
        "\t")
      
    print("Done...")
      
    print("Writing out hourly averages...")
      
    writeOutHourlyData(
        data,
        DATA_DIRECTORY + "preprocessed_hour/airquality_" + str(year) + ".csv", 
        "\t")
      
    print("Done...")
      
print("Done...")
 
 
print("Download weather data from WUnderground...")
  
for year in years:
    downloadWeatherDataFromWunderground(
        "WUKEY", 
        "UK", 
        "York", 
        generateDatesStringForYear(year), 
        DATA_DIRECTORY + "weather/wu/", 
        8.0,
        "\t")
    
print("Done...")
     
print("Processing WU weather data...")
      
for year in years: 
    processWUData(
        generateTimestamps(year),
        DATA_DIRECTORY + "weather/wu/", 
        DATA_DIRECTORY + "preprocessed_hour/stations_rectangles.csv",
        DATA_DIRECTORY + "preprocessed_hour/weather_" + str(year) + ".csv", 
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
       
for year in years:
                
    filesToJoin = [
        DATA_DIRECTORY + "preprocessed_hour/traffic_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/topo_timestamp_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/osmlanduse_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/airquality_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/weather_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/yorktime_" + str(year) + ".csv"]
                
    joinFiles(
        filesToJoin,
        DATA_DIRECTORY + "data_hour_" + str(year) + ".csv",
        False,
        "\t")
            
print("Done...")
   
print("Joining preprocessed files (binned)...")
         
for year in years:
                  
    filesToJoin = [
        DATA_DIRECTORY + "preprocessed_hour/traffic_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/topo_timestamp_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/osmlanduse_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/airquality_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/weather2_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/yorktime2_" + str(year) + ".csv"]
                  
    joinFiles(
        filesToJoin,
        DATA_DIRECTORY + "data2_hour_" + str(year) + ".csv",
        False,
        "\t")
             
print("Done...")

print("Joining preprocessed files (w/ atc data)...")
         
for year in [2013]:
                  
    filesToJoin = [
        DATA_DIRECTORY + "preprocessed_hour/traffic_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/topo_timestamp_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/osmlanduse_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/airquality_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/weather_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/yorktime_" + str(year) + ".csv",
        DATA_DIRECTORY + "preprocessed_hour/atc_" + str(year) + ".csv"
        ]
                      
    joinFiles(
        filesToJoin,
        DATA_DIRECTORY + "data3_hour_" + str(year) + ".csv",
        False,
        "\t")
             
print("Done...")
