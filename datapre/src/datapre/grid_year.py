from rectangles import createStationRectangles, generateGridStationRectangles
from topobuildings import generateRectangleBuildings
from osmpolygons import getRectangleOSMPolygons
from traffic import createRectangleTrafficAnnual
from join import joinYearForApply

DATA_DIRECTORY = "/media/sf_lur/data/"

years = [2015]
ranges = ["100", "250", "500"]

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
  
print("Creating station rectangles (100m, 250m, 500m)...")
 
for r in ranges:
  
    createStationRectangles(
        float(r), 
        DATA_DIRECTORY + "grid/stations.csv", 
        DATA_DIRECTORY + "grid/stations_rect_" + r + ".csv",
        DATA_DIRECTORY + "gis/grid_" + r + ".csv",
        "\t")
  
print("Done...")
 
print("Generating Topo buildings for rect 100m, 250m, 500m...")

for r in ranges:
    generateRectangleBuildings(
        DATA_DIRECTORY + "topo/buildings_2015.csv",
        DATA_DIRECTORY + "grid/stations_rect_" + r + ".csv",
        None,
        None,
        DATA_DIRECTORY + "preprocessed_grid/topo_" + r + "_2015.csv",
        100,
        "\t")
  
print("Done...")

   
print("Process osm polygon data for station for each year...")
for r in ["100", "250"]:
    for year in years: 
        getRectangleOSMPolygons(
            DATA_DIRECTORY + "osm/osmpoly_" + str(year) + ".csv",
            DATA_DIRECTORY + "grid/stations_rect_" + r + ".csv",
            DATA_DIRECTORY + "preprocessed_grid/osmpoly_" + r + "_" + str(year) + ".csv",
            DATA_DIRECTORY + "temp5.txt",
            "\t")
     
print("Done")

  
print("Processing traffic information for station rectangles...")
for year in years:
    for r in ["500"]:      
        createRectangleTrafficAnnual(
            DATA_DIRECTORY + "traffic/traffic.csv",
            DATA_DIRECTORY + "grid/stations_rect_" + r + ".csv",
            DATA_DIRECTORY + "preprocessed_grid/traffic_" + r + "_" + str(year) + ".csv",
            DATA_DIRECTORY + "temp3",
            "\t")
        
print("Done")
        
 
print("Joining data...")
 
joinYearForApply(
    ["topo", "traffic", "osmpoly"], 
    2015, 
    ["100", "250"], 
    DATA_DIRECTORY + "preprocessed_grid/",
    DATA_DIRECTORY + "data_grid.csv", 
    "\t")
 
print("Done")
