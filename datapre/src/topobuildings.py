"""
This file contains functions for loading buildings data file and converting it
for further data analysis
"""
from WGS84Coordinate import WGS84Coordinate
from rectangles import loadRectangles
from MapCoordinate import MapCoordinate
from Geometry import pointInTriangle
from Timestamp import generateTimestamps

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
        
        coordinateStrings = []
        for coordinate in building.coordinates:
            cString = str(coordinate.longitude) + " " + str(coordinate.latitude)
            coordinateStrings.append(cString)
        if coordinateStrings[0] != coordinateStrings[len(coordinateStrings) - 1]:
            coordinateStrings.append(coordinateStrings[0])
        
        firstCoordinate = True
        
        for coordinateString in coordinateStrings:
            if firstCoordinate == True:
                firstCoordinate = False
            else:
                output.write(", ")
            output.write(coordinateString)
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
    
def generateRectangleBuildings(inputBuildingFile, inputRectangleFile, outputGisFile, outputGISTriangleFile, outputFile, detailLevel, printPrefixString = ""):    
    # load buildings
    buildings = []
    loadBuildings(inputBuildingFile, buildings, printPrefixString)
        
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Matching station rectangles with buildings...")
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
        print(printPrefixString + "\tStation " + str(rectangle.ID))
        rectangleBuilding = []
        for building in buildings:
            for coordinate in building.coordinates:
                mapC = coordinate.toMapCoordinate()
                a = pointInTriangle(rectangle.cornerNW, rectangle.cornerNE, rectangle.cornerSE, mapC)
                if a == True:
                    rectangleBuilding.append(building)
                    break
                b = pointInTriangle(rectangle.cornerNW, rectangle.cornerSE, rectangle.cornerSW, mapC)
                if b == True:
                    rectangleBuilding.append(building)
                    break
                
                """            
            a = pointInTriangle(rectangle.cornerNW, rectangle.cornerNE, rectangle.cornerSE, building.cc)
            b = pointInTriangle(rectangle.cornerNW, rectangle.cornerSE, rectangle.cornerSW, building.cc)
            if a == True or b == True:
                rectangleBuilding.append(building)
                """        
        rectangle.buildings = rectangleBuilding
        
    print(printPrefixString + "Done...")
    
    rectangleBuildings = []
    for rectangle in rectangles:
        for building in rectangle.buildings:
            rectangleBuildings.append(building)
            
    # create gis file
    print(printPrefixString + "Writing out gis data to " + outputGisFile)
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
    print(printPrefixString + "Done...")
    
    # create triangle gis file
    print(printPrefixString + "Writing out triangle gis data to " + outputGISTriangleFile)
    output = open(outputGISTriangleFile, 'w')
    triangleId = 0
    output.write("id;polygon\n")
    
    for building in rectangleBuildings:
        building.triangles = []
        for i in range(0, len(building.coordinates) - 2):
            v1 = building.coordinates[0].toWGS84Coordinate()
            v2 = building.coordinates[i + 1].toWGS84Coordinate()
            v3 = building.coordinates[i + 2].toWGS84Coordinate()
            building.triangles.append([v1.toMapCoordinate(), v2.toMapCoordinate(), v3.toMapCoordinate()])
            triangleId = triangleId + 1
            output.write(str(triangleId) + ";")
            output.write("POLYGON((")
            output.write(str(v1.longitude) + " ")
            output.write(str(v1.latitude) + ",")
            output.write(str(v2.longitude) + " ")
            output.write(str(v2.latitude) + ",")
            output.write(str(v3.longitude) + " ")
            output.write(str(v3.latitude) + ",")
            output.write(str(v1.longitude) + " ")
            output.write(str(v1.latitude))
            output.write("))\n")
    output.close()
    print(printPrefixString + "Done...")

    print(printPrefixString + "Writing out the main output file (doing covered area) to " + outputFile + "...")
    # create output file
    output = open(outputFile, 'w')
    output.write("location,timestamp,buildings_number,buildings_area\n")
    
    timestamps = generateTimestamps(2013)
    
    for rectangle in rectangles:
        print(printPrefixString + "\tStation: " + str(rectangle.ID))
        areaCoverred = 0
        # try to find out how much part of the rectangle is covered by the buildings
        for x in range(0, detailLevel):
            for y in range(0, detailLevel):
                nw = rectangle.cornerNW.toMapCoordinate()
                se = rectangle.cornerSE.toMapCoordinate()
                # p1 = local nw, p2 = local se
                p1x = se.x + (nw.x - se.x) * (float(x) / float(detailLevel))
                p2x = se.x + (nw.x - se.x) * (float(x + 1) / float(detailLevel))
                p1y = se.y + (nw.y - se.y) * (float(y) / float(detailLevel))
                p2y = se.y + (nw.y - se.y) * (float(y + 1) / float(detailLevel))
                c = MapCoordinate((p1x + p2x) / 2.0, (p1y + p2y) / 2.0)
                
                for building in rectangle.buildings:
                    for triangle in building.triangles:
                        v1 = triangle[0]
                        v2 = triangle[1]
                        v3 = triangle[2]
                        if pointInTriangle(v1, v2, v3, c) == True:
                            areaCoverred = areaCoverred + 1
        
        coverage = float(areaCoverred)/(detailLevel * detailLevel)
        for timestamp in timestamps: 
            output.write(str(rectangle.ID) + "," + timestamp.key + "," + str(len(rectangle.buildings)) + "," + str(coverage) + "\n")
            
    output.close()
    print(printPrefixString + "Done...")
