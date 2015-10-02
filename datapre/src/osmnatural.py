import xml.etree.ElementTree as ET
from WGS84Coordinate import WGS84Coordinate
import os

class Landuse:
    def __init__(self, ID, category, coordinates):
        self.ID = ID
        self.category = category
        self.coordinates = coordinates
        
def getLanduseFromFile(fileName, landuses):
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
        isLanduse = False
        keyValue = ""
        for tag in way.findall('tag'):
            if tag.get('k') == 'landuse':
                keyValue = tag.get("v")
                isLanduse = True
        if isLanduse == False:
            continue
        landuseCoordinates = []
        for nd in way.findall('nd'):
            ID = int(nd.get('ref'))
            landuseCoordinates.append(coordinates[ID])
        landuse = Landuse(int(way.get('id')), keyValue, landuseCoordinates)
        landuses[landuse.ID] = landuse

def getLandusesFromOSM(inputOSMDirectory, outputGISFile, printPrefixString = ""):
    
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")
    
    landuses = {}
    
    fileNames = next(os.walk(inputOSMDirectory))[2]
    for fileName in fileNames:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        getLanduseFromFile(absoluteFileName, landuses)
        
    print("\r" + printPrefixString + "Loading files is done...                                              ")
    print(printPrefixString + "#landuses: " + str(len(landuses)))
    
    saveAllLandusesGis(landuses, outputGISFile, printPrefixString)
    
def saveAllLandusesGis(landuses, fileName, printPrefixString = ""):
    
    print(printPrefixString + "Saving GIS information for landuses to " + fileName + "...")
    
    # create output file
    output = open(fileName, 'w')
    output.write("id;category;polygon\n")
    
    for ID in landuses:
        landuse = landuses[ID]
        output.write(str(landuse.ID) + ";")
        output.write(landuse.category + ";")
        output.write("POLYGON((")
        
        coordinateStrings = []
        for coordinate in landuse.coordinates:
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
