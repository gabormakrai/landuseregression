"""
York hourly data prep main script file
 - downloads data where necessary
 - converts raw data files into a format
 - then joins them into one file
 - the script does it for four years (2012,2013,2014,2015)
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
from osmpolygons import getRectangleOSMPolygons, multiplyLanduseData2
from airquality import processAirQualityFiles, writeOutHourlyData
from atc import processAtcData
from osmgrabber import getPolygonsFromOSM, writeOutYearPolygons

DATA_DIRECTORY = "/home/makrai/data/york/"
OUTPUT_DIRECTORY = "/home/makrai/data/york_hour/"
OUTPUT2_DIRECTORY = "/home/makrai/data/"
 
years = [2012, 2013, 2014, 2015]

print("Create rectangles for monitoring stations...")
     
createStationRectangles(
    100.0, 
    DATA_DIRECTORY + "stations/stations_withoutbootham.csv",
    OUTPUT_DIRECTORY + "stations_rectangles.csv",
    OUTPUT_DIRECTORY + "gis/station_rectangles.csv",
    "\t")
     
print("Done...")
    
print("Creating traffic gis information file...")
     
createTrafficGISFile(
    OUTPUT_DIRECTORY + "stations_rectangles.csv",
    DATA_DIRECTORY + "traffic/traffic.csv",
    OUTPUT_DIRECTORY + "gis/traffic.csv",
    "\t")
     
print("Done...")
  
print("Processing traffic information for station rectangles...")
     
createRectangleTraffic(
    DATA_DIRECTORY + "traffic/traffic.csv",
    OUTPUT_DIRECTORY + "stations_rectangles.csv",
    OUTPUT_DIRECTORY + "traffic.csv",
    OUTPUT_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t")
     
print("Done...")
    
print("Add timestamps to traffic data...")
for year in years:
    addTimestampToTraffic(
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "traffic.csv", 
        OUTPUT_DIRECTORY + "traffic_" + str(year) + ".csv", 
        "\t")
      
print("Done...")
       
print("Processing OS Mastermap Topo layer for buildings...")
    
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2012.csv",
    OUTPUT_DIRECTORY + "gis/buildings_2012.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2013.csv",
    OUTPUT_DIRECTORY + "gis/buildings_2013.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2014.csv",
    OUTPUT_DIRECTORY + "gis/buildings_2014.csv",
    "\t")
generateAllBuildingGisInformation(
    DATA_DIRECTORY + "topo/buildings_2015.csv",
    OUTPUT_DIRECTORY + "gis/buildings_2015.csv",
    "\t")
    
print("Done...")
     
print("Processing OS Mastermap Topo layer for buildings for station rectangles...")
for year in years:   
    generateRectangleBuildings(
        DATA_DIRECTORY + "topo/buildings_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        OUTPUT_DIRECTORY + "gis/station_buildings.csv",
        OUTPUT_DIRECTORY + "gis/station_buildings_triangles.csv",
        OUTPUT_DIRECTORY + "topo_" + str(year) + ".csv",
        100,
        "\t")
                   
print("Done...")
    
print("Add timestamp to static topo building data...")
    
for year in years: 
    multiplyBuildingData(
        OUTPUT_DIRECTORY + "topo_" + str(year) + ".csv", 
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "topo_timestamp_" + str(year) + ".csv", 
        "\t")
      
print("Done...")
  
print("Processing downloaded osm data...")
  
getPolygonsFromOSM(
    DATA_DIRECTORY + "osm/downloaded/",
    DATA_DIRECTORY + "osm/history/",
    OUTPUT_DIRECTORY + "polygons.csv",
    "\t")
  
print("Done...")
  
print("Genearing polygons for each year")
   
for year in years:
    writeOutYearPolygons(
        OUTPUT_DIRECTORY + "polygons.csv", 
        year, 
        OUTPUT_DIRECTORY + "osmpoly_" + str(year) + ".csv", 
        OUTPUT_DIRECTORY + "gis/osmpoly_" + str(year) + ".csv", 
        "\t")
   
print("Done...")
     
print("Processing osm data for landuses...")
for year in years:
    getRectangleOSMPolygons(
        OUTPUT_DIRECTORY + "osmpoly_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        "landuse",
        False,
        OUTPUT_DIRECTORY + "osm_landuse_" + str(year) +".csv",
        OUTPUT_DIRECTORY + "gis/stations_landuse.csv",                
        "\t")
    getRectangleOSMPolygons(
        OUTPUT_DIRECTORY + "osmpoly_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        "leisure",
        False,
        OUTPUT_DIRECTORY + "osm_leisure_" + str(year) +".csv",
        OUTPUT_DIRECTORY + "gis/stations_landuse.csv",                
        "\t")
         
print("Done")
      
print("Add timestamp to static osm poly data...")
for year in years:
    multiplyLanduseData2(
        OUTPUT_DIRECTORY + "osm_landuse_" + str(year) + ".csv", 
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "osmlanduse_" + str(year) + ".csv", 
        "\t")
    multiplyLanduseData2(
        OUTPUT_DIRECTORY + "osm_leisure_" + str(year) + ".csv", 
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "osmleisure_" + str(year) + ".csv", 
        "\t")
print("Done")
         
print("Creating time related dataset...")
    
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        OUTPUT_DIRECTORY + "yorktime_" + str(year) +".csv",
        "\t")
      
print("Done...")
    
print("Creating time related dataset (binned)...")
     
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        OUTPUT_DIRECTORY + "yorktime2_" + str(year) +".csv",
        "\t",
        binned=True)
       
print("Done...")
    
print("Processing data air quality files...")
    
for year in years:     
    print("Loading data air quality data...")
    data = processAirQualityFiles(
        "no2", 
        [year], 
        OUTPUT_DIRECTORY + "stations_rectangles.csv", 
        DATA_DIRECTORY + "aq/", 
        "\t")
        
    print("Done...")
        
    print("Writing out hourly averages...")
        
    writeOutHourlyData(
        data,
        OUTPUT_DIRECTORY + "airquality_" + str(year) + ".csv", 
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
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        OUTPUT_DIRECTORY + "weather_" + str(year) + ".csv", 
        "\t")
         
print("Done...")
   
print("Processing WU weather data (binned)...")
         
for year in years: 
    processWUData(
        generateTimestamps(year),
        DATA_DIRECTORY + "weather/wu/", 
        OUTPUT_DIRECTORY + "stations_rectangles.csv",
        OUTPUT_DIRECTORY + "weather2_" + str(year) + ".csv", 
        "\t",
        fileList = None,
        binned=True)
          
print("Done...")
  
print("Processing ATC data...")
  
for year in years:
    processAtcData(
        year,
        OUTPUT_DIRECTORY + "stations_rectangles.csv", 
        DATA_DIRECTORY + "atc/",
        OUTPUT_DIRECTORY + "atc_" + str(year) + ".csv", 
        "\t")
  
print("Done...")
    
print("Joining preprocessed files...")
         
for year in years:
                  
    filesToJoin = [
        OUTPUT_DIRECTORY + "traffic_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "airquality_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "weather_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "yorktime_" + str(year) + ".csv"]
                  
    joinFiles(
        filesToJoin,
        OUTPUT2_DIRECTORY + "york_hour_" + str(year) + ".csv",
        False,
        "\t")
              
print("Done...")
     
print("Joining preprocessed files (binned)...")
           
for year in years:
                    
    filesToJoin = [
        OUTPUT_DIRECTORY + "traffic_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "airquality_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "weather2_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "yorktime2_" + str(year) + ".csv"]
                    
    joinFiles(
        filesToJoin,
        OUTPUT2_DIRECTORY + "york2_hour_" + str(year) + ".csv",
        False,
        "\t")
               
print("Done...")
  
print("Joining preprocessed files (w/ atc data)...")
           
for year in [2013]:
                    
    filesToJoin = [
        OUTPUT_DIRECTORY + "traffic_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "airquality_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "weather_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "yorktime_" + str(year) + ".csv",
        OUTPUT_DIRECTORY + "atc_" + str(year) + ".csv"
        ]
                        
    joinFiles(
        filesToJoin,
        OUTPUT2_DIRECTORY + "york3_hour_" + str(year) + ".csv",
        False,
        "\t")
               
print("Done...")
