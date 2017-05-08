from topobuildings import generateRectangleBuildings
from rectangles import createStationRectangles
from osmgrabber import downloadOsmData, getPolygonsFromOSM, writeOutYearPolygons
from airquality import processAirQualityFiles, writeOutAnnualAverages
from traffic import createRectangleTrafficAnnual
from osmpolygons import getRectangleOSMPolygons
from join import joinYear

DATA_DIRECTORY = "/home/makrai/data/york/"
WORK_DIRECTORY = "/home/makrai/data/york_annual/"
OUTPUT_DIRECTORY = "/home/makrai/data/" 

years = [2012, 2013, 2014, 2015] 
ranges = ["100", "250", "500"]

print("Creating station rectangles in radius 100m, 250m, 500m...")
   
for r in ranges:
    createStationRectangles(
        float(r), 
        DATA_DIRECTORY + "stations/stations.csv",
        WORK_DIRECTORY + "rectangles_" + r + ".csv",
        WORK_DIRECTORY + "gis/rectangles_" + r + ".csv",
        "\t")
       
print("Done...")
    
print("Parsing topo building data for all the radius (100,250,500) and for all years...")
  
for year in years:
    for r in ranges:
        generateRectangleBuildings(
            DATA_DIRECTORY + "topo/buildings_" + str(year) + ".csv",
            WORK_DIRECTORY + "rectangles_" + r + ".csv",
            None,
            None,
            WORK_DIRECTORY + "topo_" + r + "_" + str(year) + ".csv",
            100,
            "\t")
   
print("Done...")
   
print("Loading data air quality data...")
      
data = processAirQualityFiles(
    "no2", 
    years, 
    WORK_DIRECTORY + "rectangles_100.csv", 
    DATA_DIRECTORY + "aq/", 
    "\t")
     
print("Done...")
     
print("Writing out annaul averages...")
     
writeOutAnnualAverages(
    data, 
    years,
    WORK_DIRECTORY + "aq.csv", 
    "\t")
     
print("Done...")
    
print("Downloading osm data...")
    
downloadOsmData(-1.35, -0.83, 53.76, 54.09, DATA_DIRECTORY + "osm/downloaded/")
    
print("Done...")
   
print("Process osm data...")
     
getPolygonsFromOSM(
    DATA_DIRECTORY + "osm/downloaded/", 
    DATA_DIRECTORY + "osm/history/", #historyDirectory 
    WORK_DIRECTORY + "polygons.csv", 
    "\t")
     
print("Done...")
    
print("Process year osm polygon data...")
     
for year in years:
    writeOutYearPolygons(
        WORK_DIRECTORY + "polygons.csv", 
        year, 
        WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv", 
        WORK_DIRECTORY + "gis/osmpoly_" + str(year) + ".csv", 
        "\t")
     
print("Done...")
     
print("Process osm polygon data for station for each year...")
for r in ["100", "250", "500"]:
    for year in years: 
        getRectangleOSMPolygons(
            WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv",
            WORK_DIRECTORY + "rectangles_" + r + ".csv",
            "landuse",
            False,
            WORK_DIRECTORY + "osmlanduse_" + r + "_" + str(year) + ".csv",
            WORK_DIRECTORY + "gis/temp.txt",
            "\t")
        getRectangleOSMPolygons(
            WORK_DIRECTORY + "osmpoly_" + str(year) + ".csv",
            WORK_DIRECTORY + "rectangles_" + r + ".csv",
            "leisure",
            False,
            WORK_DIRECTORY + "osmleisure_" + r + "_" + str(year) + ".csv",
            WORK_DIRECTORY + "gis/temp.txt",
            "\t")
       
print("Done")
      
print("Processing traffic information for station rectangles...")
for year in years:
    for r in ["100", "250", "500"]:      
        createRectangleTrafficAnnual(
            DATA_DIRECTORY + "traffic/traffic.csv",
            WORK_DIRECTORY + "rectangles_" + r + ".csv",
            WORK_DIRECTORY + "traffic_" + r + "_" + str(year) + ".csv",
            WORK_DIRECTORY + "gis/temp.txt",
            "\t")
       
print("Done")
   
print("Joining the data...")
    
joinYear(
    ["traffic", "osmlanduse", "osmleisure", "topo"], 
    years, 
    ["100", "250", "500"], 
    WORK_DIRECTORY,
    OUTPUT_DIRECTORY + "york_year.csv",
    "\t")
    
print("Done")

