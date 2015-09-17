"""
This script is creating buffer rectangles for each air quality monitoring
station. 
It loads the file DATA_DIRECTORY/stations/stations.csv and creates the file
DATA_DIRECTORY/stations/station_rectangles.csv
The input file should contains a header line and the following columns in order:
id,name,latitude,longitude
"""

from directories import DATA_DIRECTORY
from MapCoordinate import MapCoordinate
from WGS84Coordinate import WGS84Coordinate

class Station:
    def __init__(self, ID, name, latitude, longitude):
        self.ID = ID
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    def toString(self):
        return "Station(id:" + str(self.ID) + ",name:" + str(self.name) + ",lat:" + str(self.latitude) + "lng:" + str(self.longitude) + ")"

rectangleSize = 100.0

inputFile = DATA_DIRECTORY + "stations/stations.csv"
outputFile = DATA_DIRECTORY + "stations/stations_rectangles.csv"
outputGISFile = DATA_DIRECTORY + "gis/station_rectangles.csv"

stations = []

firstLine = True
# open the file
with open(inputFile) as infile:
    # read line by line
    for line in infile:
        # skip the first line (header line)
        if firstLine == True:
            firstLine = False
            continue
        # remove newline character from the end
        line = line.rstrip()
        # split the line
        splittedLine = line.split(',')
        station = Station(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3])
        stations.append(station)

# function that calculates the buffer rectangle corners
def addCorners(station):
    coordinate = WGS84Coordinate(station.latitude, station.longitude)
    delta = 0.001
    mapCoordinate = coordinate.toMapCoordinate()
    #print("mC: " + mapCoordinate.toString())
    mapCoordinateX = MapCoordinate(mapCoordinate.x + delta, mapCoordinate.y)
    mapCoordinateY = MapCoordinate(mapCoordinate.x, delta + mapCoordinate.y)
    distanceX = mapCoordinate.distance(mapCoordinateX)
    distanceY = mapCoordinate.distance(mapCoordinateY)
    #print("distanceX: " + str(distanceX) + ", distanceY: " + str(distanceY))
    deltaX = delta / distanceX * (rectangleSize / 2.0)
    deltaY = delta / distanceY * (rectangleSize / 2.0)
    #print("dX: " + str(deltaX) + ", dY: " + str(deltaY))    
    station.northWestCorner = MapCoordinate(mapCoordinate.x - deltaX, mapCoordinate.y - deltaY).toWGS84Coordinate()
    station.northEastCorner = MapCoordinate(mapCoordinate.x + deltaX, mapCoordinate.y - deltaY).toWGS84Coordinate()
    station.southWestCorner = MapCoordinate(mapCoordinate.x - deltaX, mapCoordinate.y + deltaY).toWGS84Coordinate()
    station.southEastCorner = MapCoordinate(mapCoordinate.x + deltaX, mapCoordinate.y + deltaY).toWGS84Coordinate()
    #print("distance(nw,ne): " + str(station.northEastCorner.distance(station.northWestCorner)))
    #print("distance(coordinate,sw): " + str(coordinate.distance(station.southWestCorner)))
    #print("distance(coordinate,ne): " + str(coordinate.distance(station.northEastCorner)))
    #print("distance(coordinate,se): " + str(coordinate.distance(station.southEastCorner)))

# add buffer rectangles to all stations
for station in stations:
    #print(station.toString())
    addCorners(station)

# create output file
output = open(outputFile, 'w')
output.write("id,nw_latitude,nw_longitude,ne_latitude,ne_longitude,sw_latitude,sw_longitude,se_latitude,se_longitude\n")

for station in stations:
    output.write(str(station.ID) + ",")
    output.write(str(station.northWestCorner.latitude) + ",")
    output.write(str(station.northWestCorner.longitude) + ",")
    output.write(str(station.northEastCorner.latitude) + ",")
    output.write(str(station.northEastCorner.longitude) + ",")
    output.write(str(station.southWestCorner.latitude) + ",")
    output.write(str(station.southWestCorner.longitude) + ",")
    output.write(str(station.southEastCorner.latitude) + ",")
    output.write(str(station.southEastCorner.longitude) + "\n")
    
output.close()

# create gis outputfile

output = open(outputGISFile, 'w')
output.write("id;name;polygon\n")

for station in stations:
    output.write(str(station.ID) + ";")
    output.write(str(station.name) + ";")
    output.write("POLYGON((")
    output.write(str(station.northWestCorner.longitude) + " ")
    output.write(str(station.northWestCorner.latitude) + ",")
    output.write(str(station.northEastCorner.longitude) + " ")
    output.write(str(station.northEastCorner.latitude) + ",")
    output.write(str(station.southEastCorner.longitude) + " ")
    output.write(str(station.southEastCorner.latitude) + ",")
    output.write(str(station.southWestCorner.longitude) + " ")
    output.write(str(station.southWestCorner.latitude) + ",")
    output.write(str(station.northWestCorner.longitude) + " ")
    output.write(str(station.northWestCorner.latitude) + "))\n")
output.close()