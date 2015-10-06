import xml.etree.ElementTree as ET
from WGS84Coordinate import WGS84Coordinate
import os
from rectangles import loadRectangles
from Geometry import pointInTriangle
from Timestamp import generateTimestamps
from MapCoordinate import MapCoordinate
 
class OsmPolygon:
    def __init__(self, ID, category, coordinates):
        self.ID = ID
        self.category = category
        self.coordinates = coordinates
         
def getPolygonsFromFile(fileName, polygons, keys):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fileName, parser = parser)
    root = tree.getroot()
     
    coordinates = {}
     
    for element in root.findall('node'):
        longitude = element.get('lon')
        latitude = element.get('lat')
        ID = int(element.get('id'))
        coordinates[ID] = WGS84Coordinate(latitude, longitude)
         
    for way in root.findall('way'):
        isInteresting = False
        keyValue = ""
        for tag in way.findall('tag'):
            if tag.get('k') in keys:
                keyValue = tag.get("k") + "/" + tag.get("v")
                isInteresting = True
        if isInteresting == False:
            continue
        polygonCoordinates = []
        for nd in way.findall('nd'):
            ID = int(nd.get('ref'))
            polygonCoordinates.append(coordinates[ID])
        polygon = OsmPolygon(int(way.get('id')), keyValue, polygonCoordinates)
        polygons[polygon.ID] = polygon
 
def getPolygonsFromOSM(inputOSMDirectory, inputRectangleFile, outputFile, outputGISFile, outputCategoryFile, outputStationPolyGisFile, outputStationTraingleGisFile, printPrefixString = ""):
     
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")

    keys = set()
    keys.add("landuse")
    keys.add("leisure")
    keys.add("natural")
         
    polygons = {}
     
    fileNames = next(os.walk(inputOSMDirectory))[2]
    for fileName in fileNames:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        
        getPolygonsFromFile(absoluteFileName, polygons, keys)
         
    print("\r" + printPrefixString + "Loading files is done...                                              ")
    print(printPrefixString + "#polygons: " + str(len(polygons)))
    
    saveDownAllCategory(outputCategoryFile, polygons, printPrefixString)
     
    saveAllPolygonsGis(polygons, outputGISFile, printPrefixString)
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    # calculating stations polygons
    matchingStationPolygons(rectangles, polygons, printPrefixString)
    
    # write out all station related polygons GIS info
    saveStationsPolygonsGis(rectangles, outputStationPolyGisFile, printPrefixString)    
    
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
    
    timestamps = generateTimestamps(2013)
    
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
        
        for timestamp in timestamps: 
            output.write(str(rectangle.ID) + "," + timestamp.key + "," + str(landuseCoverage) + "," + str(leisureCoverage) + "\n")
            
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
