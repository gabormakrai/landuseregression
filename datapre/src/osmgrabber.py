import xml.etree.ElementTree as ET
import wget
from WGS84Coordinate import WGS84Coordinate
import os

class OsmPolygonVersion:
    def __init__(self, ID, category):
        self.ID = ID
        self.category = category
        self.versions = 0
        self.dates = []
        self.coordinates = []
    def addVersion(self, date, coordinates):
        self.versions = self.versions + 1
        self.dates.append(date)
        self.coordinates.append(coordinates)

def downloadOsmData(minLon, maxLon, minLat, maxLat, directory, printPrefixString = ""):
    
    scale = 0.01
    
    maxFile = 0
    
    lon = minLon
    while True:
        if lon > maxLon + scale:
            break
        
        lat = minLat
        while True:
            if lat > maxLat + scale:
                break
            
            maxFile = maxFile + 1
            lat = lat + scale / 2.0
        
        lon = lon + scale / 2.0       

    fileCounter = 0
    
    lon = minLon
    while True:
        if lon > maxLon + scale:
            break
        
        lat = minLat
        while True:
            if lat > maxLat + scale:
                break
            
            lon1 = lon
            lon2 = lon + scale
            lat1 = lat
            lat2 = lat + scale
            
            if os.path.exists(directory + str(fileCounter) + ".osm"):
                print("File " + directory + str(fileCounter) + ".osm exists")
            else:
                url = "http://api.openstreetmap.org/api/0.6/map?bbox=" + str(lon1) + "," + str(lat1) + "," + str(lon2) + "," + str(lat2);
                            
                while True:
                    try:
                        wget.download(url, directory + str(fileCounter) + ".osm")
                        break
                    except:
                        print
                        print("error occourd: " + str(fileCounter))
                        print
                        print
                        pass
                
                print("\r" + printPrefixString + "Downloaded: " + str(fileCounter) + " / " + str(maxFile) + "                  ", end = "")
            
            fileCounter = fileCounter + 1
            
            lat = lat + scale / 2.0
        
        lon = lon + scale / 2.0
        
def getPolygonsFromFile(fileName, polygons, polygonsWithHistory, keys, coordinates):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fileName, parser = parser)
    root = tree.getroot()
     
    for element in root.findall('node'):
        longitude = element.get('lon')
        latitude = element.get('lat')
        ID = str(element.get('id'))
        coordinates[ID] = WGS84Coordinate(latitude, longitude)
         
    for way in root.findall('way'):
        isInteresting = False
        keyValue = ""
        version = way.get('version')
        for tag in way.findall('tag'):
            if tag.get('k') in keys:
                keyValue = tag.get("k") + "/" + tag.get("v")
                isInteresting = True
        if isInteresting == False:
            continue
        if version == "1" or polygonsWithHistory == None:
            polygonCoordinates = []
            for nd in way.findall('nd'):
                ID = str(nd.get('ref'))
                polygonCoordinates.append(coordinates[ID])
            polygon = OsmPolygonVersion(int(way.get('id')), keyValue)
            polygon.addVersion(way.get('timestamp'), polygonCoordinates)
            polygons[polygon.ID] = polygon
        else:
            polygonsWithHistory.add(way.get('id'))
 
def getPolygonsFromOSM(inputOSMDirectory, historyDirectory, outputFile, printPrefixString = ""):
    
    if os.path.exists(outputFile):
        print(printPrefixString + "output file " + str(outputFile) + " exists...")
        return
     
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")

    keys = set()
    keys.add("landuse")
    keys.add("leisure")
    keys.add("natural")
         
    polygons = {}
    polygonsWithHistory = set()
    coordinates = {}
     
    fileNames = next(os.walk(inputOSMDirectory))[2]
    for fileName in fileNames:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        
        getPolygonsFromFile(absoluteFileName, polygons, polygonsWithHistory, keys, coordinates)
         
    print("\r" + printPrefixString + "Loading files is done...                                              ")
    print(printPrefixString + "#polygons: " + str(len(polygons)))
    print(printPrefixString + "#polygonsWithHistory: " + str(len(polygonsWithHistory)))
    
    print(printPrefixString + "Downloading history for polygons...")
    counter = 0
    for osmid in polygonsWithHistory:
        print(printPrefixString + "\r\tDownloading " + str(counter) + " / " + str(len(polygonsWithHistory)) + ":" + str(osmid) + "                ", end = "")
        downloadHistory(osmid, "way", historyDirectory)
        counter = counter + 1
    print()
    print(printPrefixString + "Done...")
    
    polygonsWithHistory = {}
    
    print(printPrefixString + "Parse history files...")
    fileNames = next(os.walk(historyDirectory))[2]
    for fileName in fileNames:
        if fileName[0:3] != "way":
            continue
        absoluteFileName = historyDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        
        parseHistoryOSMFile(absoluteFileName, polygonsWithHistory, keys)
        
    print()
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Find missing coordaintes...")
    
    missingCoordinates = set()
    
    findMissingCoordinates(coordinates, polygonsWithHistory, missingCoordinates)
    
    print(printPrefixString + "\t#missingCoordinates: " + str(len(missingCoordinates)))
        
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Downloading missing coordinates...")
    
    counter = 0
    for coordinate in missingCoordinates:
        print(printPrefixString + "\r\tDownloading " + str(counter) + " / " + str(len(missingCoordinates)) + ":" + str(coordinate) + "                ", end = "")
        downloadHistory(coordinate, "node", historyDirectory)
        counter = counter + 1
    
    print()
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Parsing missing coordinates files...")
    print(printPrefixString + "#coordinates: " + str(len(coordinates)))
    fileNames = next(os.walk(historyDirectory))[2]
    for fileName in fileNames:
        if fileName[0:3] != "nod":
            continue
        absoluteFileName = historyDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        
        parseMissingCoordinateFile(absoluteFileName, coordinates)
    
    print()
    print(printPrefixString + "#coordinates: " + str(len(coordinates)))
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Fill polygons with coordinates...")
    matchCoordinates(polygonsWithHistory, coordinates)
    print(printPrefixString + "Done...")
    
    # unifying the two polygon dictionary
    for polyId in polygonsWithHistory:
        polygons[polyId] = polygonsWithHistory[polyId]

    # write out polygons
    print(printPrefixString + "Write out polygons to " + outputFile + "...")
    writeOutPolygons(outputFile, polygons)
    print(printPrefixString + "Done...")

def downloadHistory(osmid, osmtype, directory):
    
    if os.path.exists(directory + osmtype + "_" + str(osmid) + ".osm"):
        return
    
    url = "http://api.openstreetmap.org/api/0.6/" + osmtype + "/" + str(osmid) + "/history";
                        
    while True:
        try:
            wget.download(url, directory + osmtype + "_" + str(osmid) + ".osm")
            break
        except:
            print
            print("error occourd: " + str(osmid))
            print
            print
            pass
        
def parseHistoryOSMFile(fileName, polygons, keys):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fileName, parser = parser)
    root = tree.getroot()
    
    firstWay = True
    
    polygon = None
      
    for way in root.findall('way'):
        if firstWay:
            firstWay = False
            keyValue = ""
            for tag in way.findall('tag'):
                if tag.get('k') in keys:
                    keyValue = tag.get("k") + "/" + tag.get("v")
            polygon = OsmPolygonVersion(way.get('id'), keyValue)
            
        polygonCoordinates = []
        for nd in way.findall('nd'):
            polygonCoordinates.append(int(nd.get('ref')))
        polygon.addVersion(way.get('timestamp'), polygonCoordinates)

    polygons[polygon.ID] = polygon
    
def findMissingCoordinates(coordinates, polygons, missingCoordinates):
    for osmid in polygons:
        polygon = polygons[osmid]
        for polyCoordinates in polygon.coordinates:
            for coord in polyCoordinates:
#                 if str(coord) == "1305972367":
#                     print("hello")
#                     print(str(coordinates["1305972367"]))
                if coord not in coordinates:
                    missingCoordinates.add(str(coord))
    
def parseMissingCoordinateFile(fileName, coordinates):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fileName, parser = parser)
    root = tree.getroot()
    
    nodeId = ""
    nodeLongitude = 0.0
    nodeLatitude = 0.0
      
    for node in root.findall('node'):
        nodeId = str(node.get("id"))
        if node.get("lat") != None:
            nodeLongitude = node.get("lon")
            nodeLatitude = node.get("lat")

#     print("nodeId: " + str(nodeId))
#     print("nodeLongitude: " + str(nodeLongitude))
#     print("nodeLatitude: " + str(nodeLatitude))    
    
    coordinates[nodeId] = WGS84Coordinate(nodeLatitude, nodeLongitude)

def matchCoordinates(polygons, coordinates):
    for osmid in polygons:
        polygon = polygons[osmid]
        newCoordinateList = []
        for polyCoordinates in polygon.coordinates:
            newPolyCoordinates = []
            for coord in polyCoordinates:
                newPolyCoordinates.append(coordinates[str(coord)])
            newCoordinateList.append(newPolyCoordinates)
        polygon.coordinates = newCoordinateList

def writeOutPolygons(fileName, polygons):
    output = open(fileName, 'w')
    output.write("id,category,date,shape\n")
    for polyId in polygons:
        polygon = polygons[polyId]
        for i in range(0, polygon.versions):
            output.write(str(polyId) + "," + str(polygon.category) + ",")
            output.write(str(polygon.dates[i]) + ",")
            shape = str(polygon.coordinates[i][0].latitude) + ";" + str(polygon.coordinates[i][0].longitude) 
            for j in range(1, len(polygon.coordinates[i])):
                shape = shape + ";" + str(polygon.coordinates[i][j].latitude) + ";" + str(polygon.coordinates[i][j].longitude) 
            output.write(shape + "\n")

def loadPolygons(fileName, printPrefixString = ""):
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
            date = str(splittedLine[2])
            shape = str(splittedLine[3])
            
            splittedShape = shape.split(";")
            coordinates = []
            for i in range(0, int(len(splittedShape) / 2)):
                lat = splittedShape[2 * i]
                lon = splittedShape[2 * i + 1]
                coordinates.append(WGS84Coordinate(lat, lon))
            
            polygon = None
            if polyId in polygons:
                polygon = polygons[polyId]
            else:
                polygon = OsmPolygonVersion(polyId, category)
                polygons[polyId] = polygon
                
            polygons[polyId].addVersion(date, coordinates)
            
    print(printPrefixString + "\t#polygons: " + str(len(polygons)))
    print(printPrefixString + "Done...")
    return polygons

def writeOutYearPolygons(inputPolygonFile, year, fileName, gisFileName, printPrefixString = ""):
    # load polygons
    polygons = loadPolygons(inputPolygonFile, printPrefixString)
    
    yearDate = str(year) + "-12-31T23:59:59Z"
    
    print(printPrefixString + "writing out " + str(fileName) + " poly file...")
     
    output = open(fileName, 'w')
    output.write("id,category,date,shape\n")    
     
    print(printPrefixString + "writing out " + str(fileName) + " gis file...")
    
    outputGis = open(gisFileName, 'w')
    outputGis.write("id;category;date;shape\n")    
     
    for polyId in polygons:
        polygon = polygons[polyId]
         
        shape = None
        polyDate = None
        for i in range(0, len(polygon.dates)):
            date = polygon.dates[i]
            if date < yearDate:
                shape = polygon.coordinates[i]
                polyDate = date
         
        if shape == None:
            continue
         
        output.write(str(polyId) + ",")
        output.write(str(polygon.category) + ",")
        output.write(str(polyDate) + ",")
        shapeString = str(shape[0].latitude) + ";" + str(shape[0].longitude) 
        for j in range(1, len(shape)):
            shapeString = shapeString + ";" + str(shape[j].latitude) + ";" + str(shape[j].longitude) 
 
        output.write(shapeString + "\n")
        
        outputGis.write(polyId + ";")
        outputGis.write(polygon.category + ";")
        outputGis.write(polyDate + ";")
        outputGis.write("POLYGON((")
        firstCoordinate = True
        for coordinate in shape:
            if firstCoordinate == False:
                outputGis.write(",")
            outputGis.write(str(coordinate.longitude) + " ")
            outputGis.write(str(coordinate.latitude))
            if firstCoordinate == True:
                firstCoordinate = False
        outputGis.write("))\n")
    
    output.close()
    outputGis.close()
    
    print(printPrefixString + "done...")
    
def getPolygonsWithoutHistoryFromOSM(inputOSMDirectory, outputFile, printPrefixString = "", keys = ("landuse", "leisure", "natural")):
     
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")
         
    polygonsList = []
    coordinatesList = []

    polygons = {}
    coordinates = {}
         
    fileNames = next(os.walk(inputOSMDirectory))[2]
    fileNames2 = sorted(fileNames)
    for fileName in fileNames2:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        getPolygonsFromFile(absoluteFileName, polygons, None, keys, coordinates)
        if len(polygons) > 50000:
            polygonsList.append(polygons)
            coordinatesList.append(coordinates)
            polygons = {}
            coordinates = {}
            polyCounter = 0
            for p in polygonsList:
                polyCounter = polyCounter + len(p)
            print("current:" + str(polyCounter))
         
    print("\r" + printPrefixString + "Loading files is done...                                              ")
    print(printPrefixString + "merging polygons...")
    
    for ps in polygonsList:
        for p in ps: 
            polygons[p] = ps[p]
    for cs in coordinatesList:
        for c in cs: 
            coordinates[c] = cs[c]
    
    print(printPrefixString + "#polygons: " + str(len(polygons)))
    print(printPrefixString + "#coordinates: " + str(len(coordinates)))
    
    # write out polygons
    print(printPrefixString + "Write out polygons to " + outputFile + "...")
    writeOutPolygons(outputFile, polygons)
    print(printPrefixString + "Done...")
        
def getPolygonCategoriesFromOSM(inputOSMDirectory, outputFile, printPrefixString = ""):
     
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")
         
    categories = {}
         
    fileNames = next(os.walk(inputOSMDirectory))[2]
    fileNames2 = sorted(fileNames)
    for fileName in fileNames2:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + ", #c:" + str(len(categories)) + "                        ", end = "")
        getPolygonCategoriesFromFile(absoluteFileName, categories)
    
    categoriesList = []
    for c in categories:
        if categories[c] > 10:
            categoriesList.append(c)

    sorted(categoriesList)
    
    output = open(outputFile, 'w')
    output.write("category,freq\n")
    for c in categoriesList:
        output.write(str(c) + "," + str(categories[c]) + "\n")
    
    output.close()
        
def getPolygonCategoriesFromFile(fileName, categories):
        
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fileName, parser = parser)
    root = tree.getroot()
         
    for way in root.findall('way'):
        keyValue = ""
        for tag in way.findall('tag'):
            keyValue = tag.get("k") + "/" + tag.get("v")
            keyValue = keyValue.replace(",","_")
            if keyValue not in categories:
                categories[keyValue] = 1
            else:
                f = categories[keyValue]
                f = f + 1
                categories[keyValue] = f
