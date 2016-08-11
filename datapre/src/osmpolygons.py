from WGS84Coordinate import WGS84Coordinate
from rectangles import loadRectangles
from Geometry import pointInTriangle
from MapCoordinate import MapCoordinate

class OsmPolygon:
    def __init__(self, ID, category, coordinates):
        self.ID = ID
        self.category = category
        self.coordinates = coordinates
        
def loadPolygons(fileName, printPrefixString):
    
    polygons = {}
    
    print(printPrefixString + "Loading " + fileName + " polygon file...")
    
    firstLine = True
    # open the file
    with open(fileName) as infile:
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
            
            #314867713,natural/wood,2014-11-28T14:46:26Z,53.7872633;-0.8605173;53.7872554;-0.8604771;53.7872432;-0.8604623;53.7872056;-0.860443;53.7871637;-0.8604493;53.7867152;-0.860634;53.7865587;-0.8607221;53.786546;-0.8607951;53.7865397;-0.8610242;53.7862582;-0.8610407;53.7863269;-0.8611622;53.7865431;-0.8614102;53.7866365;-0.8614155;53.7868948;-0.8612142;53.7871119;-0.860948;53.7872072;-0.8608029;53.7872608;-0.8605705;53.7872633;-0.8605173    
            polyId = str(splittedLine[0])
            category = str(splittedLine[1])
            shape = str(splittedLine[2])
            
            splittedShape = shape.split(";")
            coordinates = []
            for i in range(0, int(len(splittedShape) / 2)):
                lat = splittedShape[2 * i]
                lon = splittedShape[2 * i + 1]
                coordinates.append(WGS84Coordinate(lat, lon))
            
            polygon = OsmPolygon(polyId, category, coordinates)
            polygons[polyId] = polygon
                            
    print(printPrefixString + "\t#polygons: " + str(len(polygons)))
    print(printPrefixString + "Done...")
    return polygons
    
def getRectangleOSMPolygons(inputPolygonFile, inputRectangleFile, outputFile, outputStationTraingleGisFile, printPrefixString):
    
    polygons = loadPolygons(inputPolygonFile, printPrefixString)
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
     
    # calculating stations polygons
    matchingStationPolygons(rectangles, polygons, printPrefixString)
     
#     # write out all station related polygons GIS info
#     saveStationsPolygonsGis(rectangles, outputStationPolyGisFile, printPrefixString)    
     
    # generate station polygons triangles
    createTriangleAndSaveFiles(rectangles, outputFile, 100, outputStationTraingleGisFile, printPrefixString)
  
         
     
def createTriangleAndSaveFiles(rectangles, outputFile, detailLevel, outputGISTriangleFile, printPrefixString = ""):
     
    print(printPrefixString + "Writing out triangle gis data to " + outputGISTriangleFile)
    output = open(outputGISTriangleFile, 'w')
    triangleId = 0
    output.write("id;polygon\n")
    for rectangle in rectangles:
        for polygon in rectangle.polygons:
            polygon.triangles = []
            for i in range(0, len(polygon.coordinates) - 2):
                v1 = polygon.coordinates[0].toWGS84Coordinate()
                v2 = polygon.coordinates[i + 1].toWGS84Coordinate()
                v3 = polygon.coordinates[i + 2].toWGS84Coordinate()
                polygon.triangles.append([v1.toMapCoordinate(), v2.toMapCoordinate(), v3.toMapCoordinate()])
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
    output.write("location,leisure_area,landuse_area\n")
    for rectangle in rectangles:
        print(printPrefixString + "\tStation: " + str(rectangle.ID))
        leisureAreaCoverred = 0
        landuseAreaCoverred = 0
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
                 
                leisureCovered = False
                landuseCovered = False
                 
                for polygon in rectangle.polygons:
                    for triangle in polygon.triangles:
                        v1 = triangle[0]
                        v2 = triangle[1]
                        v3 = triangle[2]
                        if pointInTriangle(v1, v2, v3, c) == True:
                            if polygon.category[0:7] == "leisure" and leisureCovered == False:
                                leisureAreaCoverred = leisureAreaCoverred + 1
                                leisureCovered = True
                            if polygon.category[0:7] == "landuse" and landuseCovered == False:
                                landuseAreaCoverred = landuseAreaCoverred + 1
                                landuseCovered = True
         
        landuseCoverage = float(landuseAreaCoverred)/(detailLevel * detailLevel)
        leisureCoverage = float(leisureAreaCoverred)/(detailLevel * detailLevel)
         
        output.write(str(rectangle.ID) + "," + str(landuseCoverage) + "," + str(leisureCoverage) + "\n")
             
    output.close()
    print(printPrefixString + "Done...")
         
def matchingStationPolygons(rectangles, polygons, printPrefixString = ""):
 
    print(printPrefixString + "Matching station rectangles with polygons...")
         
    # find out building rectangles
    for rectangle in rectangles:
        print(printPrefixString + "\tStation " + str(rectangle.ID))
        rectanglePolygon = []
        for ID in polygons:
            polygon = polygons[ID]
            for coordinate in polygon.coordinates:
                mapC = coordinate.toMapCoordinate()
                a = pointInTriangle(rectangle.cornerNW, rectangle.cornerNE, rectangle.cornerSE, mapC)
                if a == True:
                    rectanglePolygon.append(polygon)
                    break
                b = pointInTriangle(rectangle.cornerNW, rectangle.cornerSE, rectangle.cornerSW, mapC)
                if b == True:
                    rectanglePolygon.append(polygon)
                    break
                 
        rectangle.polygons = rectanglePolygon
         
    print(printPrefixString + "Done...")
     
def saveDownAllCategory(outputFile, polygons, printPrefixString = ""):
     
    print(printPrefixString + "Writing out categories from polygons to " + outputFile + "....")
     
    frequency = {}
     
    for pId in polygons:
        key = polygons[pId].category 
        if key not in frequency:
            frequency[key] = 1
        else:
            f = frequency[key]
            f = f + 1
            frequency[key] = f
     
    categoryArray = []
    for category in frequency:
        categoryArray.append(category)
         
    categoryArray.sort()
 
    # create output file
    output = open(outputFile, 'w')
    output.write("category,frequency\n")
     
    for c in categoryArray:
        output.write(c + "," + str(frequency[c]) + "\n")
         
    output.close()
     
    print(printPrefixString + "Done...")
     
def saveAllPolygonsGis(polygons, fileName, printPrefixString = ""):
      
    print(printPrefixString + "Saving GIS information for polygons to " + fileName + "...")
      
    # create output file
    output = open(fileName, 'w')
    output.write("id;category;polygon\n")
      
    for ID in polygons:
        polygon = polygons[ID]
        output.write(str(polygon.ID) + ";")
        output.write(polygon.category + ";")
        output.write("POLYGON((")
          
        coordinateStrings = []
        for coordinate in polygon.coordinates:
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
 
def saveStationsPolygonsGis(stations, fileName, printPrefixString = ""):
      
    print(printPrefixString + "Saving GIS information for station polygons to " + fileName + "...")
     
    polygons = []
 
    for station in stations:
        for p in station.polygons:
            polygons.append(p)
      
    # create output file
    output = open(fileName, 'w')
    output.write("id;category;polygon\n")
      
    for polygon in polygons:
        output.write(str(polygon.ID) + ";")
        output.write(polygon.category + ";")
        output.write("POLYGON((")
          
        coordinateStrings = []
        for coordinate in polygon.coordinates:
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

def multiplyLanduseData(inputFile, timestamps, outputfile, printPrefixString = ""):
    
    # open the file
    print(printPrefixString + "Open osm polygon data file " + inputFile + " and open output file " + outputfile + "...")
    
    output = open(outputfile, 'w')
    output.write("location,timestamp,leisure_area,landuse_area\n");    
    
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
            
            for timestamp in timestamps:    
                output.write(splittedLine[0]) # location
                output.write(",")
                output.write(timestamp.key)
                output.write(",")
                output.write(splittedLine[1]) # leisure_area
                output.write(",")
                output.write(splittedLine[2]) # landuse_area
                output.write("\n")
    output.close()
