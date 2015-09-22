"""
This file contains functions for loading buildings data file and converting it
for further data analysis
"""
from WGS84Coordinate import WGS84Coordinate
from rectangles import loadRectangles
from MapCoordinate import MapCoordinate
from Geometry import pointInTriangle

class Building:
    def __init__(self, osref, coordinates):
        self.osref = osref
        self.coordinates = coordinates

def generateAllBuildingGisInformation(inputFile, outputGisFile, printPrefixString = ""):    
    
    buildings = []
    loadBuildings(inputFile, buildings, printPrefixString)
    
    print(printPrefixString + "Writing out gis data to " + outputGisFile)
    
    # create output file
    output = open(outputGisFile, 'w')
    output.write("osref;polygon\n")
    
    for building in buildings:
        output.write(building.osref + ";")
        output.write("POLYGON((")
        firstCoordinate = True
        for coordinate in building.coordinates:
            if firstCoordinate == False:
                output.write(",")
            output.write(str(coordinate.longitude) + " ")
            output.write(str(coordinate.latitude))
            if firstCoordinate == True:
                firstCoordinate = False
        output.write("))\n")
    output.close()
    
    print(printPrefixString + "Done...")
    
def loadBuildings(inputFile, buildings, printPrefixString = ""):
    print(printPrefixString + "Open building data file " + inputFile)
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
            splittedLine = line.split(';')
            osref = splittedLine[0]
            coordinateString = splittedLine[1].split(',')
            
            numberOfCoordinates = int(len(coordinateString) / 2)
            coordinates = []
            for i in range(0, numberOfCoordinates - 1):
                c = WGS84Coordinate(float(coordinateString[i * 2]), float(coordinateString[i * 2 + 1]))
                coordinates.append(c)
            
            if coordinates[0].distance(coordinates[len(coordinates) - 1]) > 0.005:
                coordinates.append(coordinates[0])
        
            buildings.append(Building(osref, coordinates))

    print(printPrefixString + "#buildings: " + str(len(buildings)))
    print(printPrefixString + "Done...")
    
def generateRectangleBuildings(inputBuildingFile, inputRectangleFile, outputGisFile, outputFile, printPrefixString = ""):    
    # load buildings
    buildings = []
    loadBuildings(inputBuildingFile, buildings, printPrefixString)
        
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
        
    # calculate center point for each building
    for building in buildings:
        cx = 0.0
        cy = 0.0
        counter = 0
        firstCoordinate = True
        for c in building.coordinates:
            if firstCoordinate == True:
                firstCoordinate = False
                continue
            mapC = c.toMapCoordinate()
            cx += mapC.x
            cy += mapC.y
            counter = counter + 1
        cx = cx / float(counter)
        cy = cy / float(counter)
        building.cc = MapCoordinate(cx, cy)
    
    # find out building rectangles
    for rectangle in rectangles:
        rectangleBuilding = []
        for building in buildings:
            a = pointInTriangle(rectangle.cornerNW, rectangle.cornerNE, rectangle.cornerSE, building.cc)
            b = pointInTriangle(rectangle.cornerNW, rectangle.cornerSE, rectangle.cornerSW, building.cc)
            if a == True or b == True:
                rectangleBuilding.append(building)
        
        rectangle.buildings = rectangleBuilding
        
    rectangleBuildings = []
    for rectangle in rectangles:
        for building in rectangle.buildings:
            rectangleBuildings.append(building)
            
    # create gis file
    print(printPrefixString + "Writing out gis data to " + outputGisFile)
    
    # create output file
    output = open(outputGisFile, 'w')
    output.write("osref;polygon\n")
    
    for building in rectangleBuildings:
        output.write(building.osref + ";")
        output.write("POLYGON((")
        firstCoordinate = True
        for coordinate in building.coordinates:
            if firstCoordinate == False:
                output.write(",")
            output.write(str(coordinate.longitude) + " ")
            output.write(str(coordinate.latitude))
            if firstCoordinate == True:
                firstCoordinate = False
        output.write("))\n")
    output.close()
    