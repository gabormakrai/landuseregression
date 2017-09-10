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
from time_data import createTimeFile
from join import joinFiles
from Timestamp import generateDatesStringForYear, generateTimestamps
from weather import downloadWeatherDataFromWunderground, processWUData
from osmpolygons import getRectangleOSMPolygons, multiplyLanduseData2
from airquality import processAirQualityFiles, writeOutHourlyData
from atc import processAtcData
from osmgrabber import getPolygonsFromOSM, writeOutYearPolygons, downloadOsmData

RAW_DATA_DIRECTORY = "/data_raw/york/"
WORK_DIRECTORY = "/data/york_hour/"
OUTPUT_DIRECTORY = "/data/"

SKIP_DOWNLOAD_STEPS = True
 
years = [2012, 2013, 2014, 2015]

print("Create rectangles for monitoring stations...")
      
createStationRectangles(
    100.0, 
    RAW_DATA_DIRECTORY + "stations/stations_withoutbootham.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    WORK_DIRECTORY + "gis/station_rectangles.csv",
    "\t")
      
print("Done...")
     
print("Creating traffic gis information file...")
      
createTrafficGISFile(
    WORK_DIRECTORY + "stations_rectangles.csv",
    RAW_DATA_DIRECTORY + "traffic/traffic.csv",
    WORK_DIRECTORY + "gis/traffic.csv",
    "\t")
      
print("Done...")
   
print("Processing traffic information for station rectangles...")
      
createRectangleTraffic(
    RAW_DATA_DIRECTORY + "traffic/traffic.csv",
    WORK_DIRECTORY + "stations_rectangles.csv",
    WORK_DIRECTORY + "traffic.csv",
    WORK_DIRECTORY + "gis/stations_rectangles_traffic.csv",
    "\t")
      
print("Done...")
     
print("Add timestamps to traffic data...")
for year in years:
    addTimestampToTraffic(
        generateTimestamps(year), 
        WORK_DIRECTORY + "traffic.csv", 
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv", 
        "\t")
       
print("Done...")
        
print("Processing OS Mastermap Topo layer for buildings...")
     
generateAllBuildingGisInformation(
    RAW_DATA_DIRECTORY + "topo/buildings_2012.csv",
    WORK_DIRECTORY + "gis/buildings_2012.csv",
    "\t")
generateAllBuildingGisInformation(
    RAW_DATA_DIRECTORY + "topo/buildings_2013.csv",
    WORK_DIRECTORY + "gis/buildings_2013.csv",
    "\t")
generateAllBuildingGisInformation(
    RAW_DATA_DIRECTORY + "topo/buildings_2014.csv",
    WORK_DIRECTORY + "gis/buildings_2014.csv",
    "\t")
generateAllBuildingGisInformation(
    RAW_DATA_DIRECTORY + "topo/buildings_2015.csv",
    WORK_DIRECTORY + "gis/buildings_2015.csv",
    "\t")
     
print("Done...")
      
print("Processing OS Mastermap Topo layer for buildings for station rectangles...")
for year in years:   
    generateRectangleBuildings(
        RAW_DATA_DIRECTORY + "topo/buildings_" + str(year) + ".csv",
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "gis/station_buildings.csv",
        WORK_DIRECTORY + "gis/station_buildings_triangles.csv",
        WORK_DIRECTORY + "topo_" + str(year) + ".csv",
        100,
        "\t")
                    
print("Done...")
     
print("Add timestamp to static topo building data...")
     
for year in years: 
    multiplyBuildingData(
        WORK_DIRECTORY + "topo_" + str(year) + ".csv", 
        generateTimestamps(year), 
        WORK_DIRECTORY + "topo_timestamp_" + str(year) + ".csv", 
        "\t")
       
print("Done...")

print("Downloading osm data...")

if SKIP_DOWNLOAD_STEPS:
    print("\tSkipping download steps")
else:    
    downloadOsmData(-1.35, -0.83, 53.76, 54.09, WORK_DIRECTORY + "osm/downloaded/")
    
print("Done...")
   
print("Processing downloaded osm data...")
   
getPolygonsFromOSM(
    WORK_DIRECTORY + "osm/downloaded/",
    WORK_DIRECTORY + "osm/history/",
    WORK_DIRECTORY + "polygons.csv",
    "\t")
   
print("Done...")
   
print("Genearing polygons for each year")
    
for year in years:
    writeOutYearPolygons(
        WORK_DIRECTORY + "polygons.csv", 
        year, 
        WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv", 
        WORK_DIRECTORY + "gis/osmpoly_" + str(year) + ".csv", 
        "\t")
    
print("Done...")
      
print("Processing osm data for landuses...")
for year in years:
    getRectangleOSMPolygons(
        WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv",
        WORK_DIRECTORY + "stations_rectangles.csv",
        "landuse",
        False,
        WORK_DIRECTORY + "osm_landuse_" + str(year) +".csv",
        WORK_DIRECTORY + "gis/stations_landuse.csv",                
        "\t")
    getRectangleOSMPolygons(
        WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv",
        WORK_DIRECTORY + "stations_rectangles.csv",
        "leisure",
        False,
        WORK_DIRECTORY + "osm_leisure_" + str(year) +".csv",
        WORK_DIRECTORY + "gis/stations_landuse.csv",                
        "\t")
          
print("Done")
       
print("Add timestamp to static osm poly data...")
for year in years:
    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_landuse_" + str(year) + ".csv", 
        generateTimestamps(year), 
        WORK_DIRECTORY + "osmlanduse_" + str(year) + ".csv", 
        "\t")
    multiplyLanduseData2(
        WORK_DIRECTORY + "osm_leisure_" + str(year) + ".csv", 
        generateTimestamps(year), 
        WORK_DIRECTORY + "osmleisure_" + str(year) + ".csv", 
        "\t")
print("Done")
          
print("Creating time related dataset...")
     
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "yorktime_" + str(year) +".csv",
        "\t")
       
print("Done...")
     
print("Creating time related dataset (binned)...")
      
for year in years:  
    createTimeFile(
        generateTimestamps(year), 
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "yorktime2_" + str(year) +".csv",
        "\t",
        binned=True)
        
print("Done...")
     
print("Processing data air quality files...")
     
for year in years:     
    print("Loading data air quality data...")
    data = processAirQualityFiles(
        "no2", 
        [year], 
        WORK_DIRECTORY + "stations_rectangles.csv", 
        RAW_DATA_DIRECTORY + "aq/", 
        "\t")
         
    print("Done...")
         
    print("Writing out hourly averages...")
         
    writeOutHourlyData(
        data,
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv", 
        "\t")
         
    print("Done...")
         
print("Done...")
    
print("Download weather data from WUnderground...")

if SKIP_DOWNLOAD_STEPS:
    print("\tSkipping download steps...")
else:
    for year in years:
        downloadWeatherDataFromWunderground(
            "WUKEY", 
            "UK", 
            "York", 
            generateDatesStringForYear(year), 
            WORK_DIRECTORY + "weather/wu/", 
            8.0,
            "\t")
       
print("Done...")
        
print("Processing WU weather data...")
         
for year in years: 
    processWUData(
        generateTimestamps(year),
        WORK_DIRECTORY + "weather/wu/", 
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "weather_" + str(year) + ".csv", 
        "\t")
          
print("Done...")
    
print("Processing WU weather data (binned)...")
          
for year in years: 
    processWUData(
        generateTimestamps(year),
        WORK_DIRECTORY + "weather/wu/", 
        WORK_DIRECTORY + "stations_rectangles.csv",
        WORK_DIRECTORY + "weather2_" + str(year) + ".csv", 
        "\t",
        fileList = None,
        binned=True)
           
print("Done...")
   
print("Processing ATC data...")
   
for year in years:
    processAtcData(
        year,
        WORK_DIRECTORY + "stations_rectangles.csv", 
        RAW_DATA_DIRECTORY + "atc/",
        WORK_DIRECTORY + "atc_" + str(year) + ".csv", 
        "\t")
   
print("Done...")
     
print("Joining preprocessed files...")
          
for year in years:
                   
    filesToJoin = [
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv",
        WORK_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv",
        WORK_DIRECTORY + "weather_" + str(year) + ".csv",
        WORK_DIRECTORY + "yorktime_" + str(year) + ".csv"]
                   
    joinFiles(
        filesToJoin,
        OUTPUT_DIRECTORY + "york_hour_" + str(year) + ".csv",
        False,
        "\t")
               
print("Done...")
      
print("Joining preprocessed files (binned)...")
            
for year in years:
                     
    filesToJoin = [
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv",
        WORK_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv",
        WORK_DIRECTORY + "weather2_" + str(year) + ".csv",
        WORK_DIRECTORY + "yorktime2_" + str(year) + ".csv"]
                     
    joinFiles(
        filesToJoin,
        OUTPUT_DIRECTORY + "york2_hour_" + str(year) + ".csv",
        False,
        "\t")
                
print("Done...")
   
print("Joining preprocessed files (w/ atc data)...")
            
for year in [2013]:
                     
    filesToJoin = [
        WORK_DIRECTORY + "traffic_" + str(year) + ".csv",
        WORK_DIRECTORY + "topo_timestamp_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmlanduse_" + str(year) + ".csv",
        WORK_DIRECTORY + "osmleisure_" + str(year) + ".csv",
        WORK_DIRECTORY + "airquality_" + str(year) + ".csv",
        WORK_DIRECTORY + "weather_" + str(year) + ".csv",
        WORK_DIRECTORY + "yorktime_" + str(year) + ".csv",
        WORK_DIRECTORY + "atc_" + str(year) + ".csv"
        ]
                         
    joinFiles(
        filesToJoin,
        OUTPUT_DIRECTORY + "york3_hour_" + str(year) + ".csv",
        False,
        "\t")
                
print("Done...")
