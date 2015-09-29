import xml.etree.ElementTree as ET
from WGS84Coordinate import WGS84Coordinate
import os

class Building:
    def __init__(self, ID, category, coordinates):
        self.ID = ID
        self.category = category
        self.coordinates = coordinates
        
def getBuildingsFromOsmFile(fileName, buildings):
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
        isBuilding = False
        for tag in way.findall('tag'):
            if tag.get('k') == 'building':
                isBuilding = True
        if isBuilding == False:
            continue
        buildingCoordinates = []
        for nd in way.findall('nd'):
            ID = int(nd.get('ref'))
            buildingCoordinates.append(coordinates[ID])
        buildingCoordinates.append(buildingCoordinates[0])
        building = Building(int(way.get('id')), '?', buildingCoordinates)
        buildings[building.ID] = building

def getBuildingsFromOSM(inputOSMDirectory, outputGISFile, printPrefixString = ""):
    
    print(printPrefixString + "Opening directory " + inputOSMDirectory + " for osm files...")
    
    buildings = {}
    
    fileNames = next(os.walk(inputOSMDirectory))[2]
    for fileName in fileNames:
        absoluteFileName = inputOSMDirectory + fileName
        print("\r" + printPrefixString + "processing file: " + absoluteFileName + "                        ", end = "")
        getBuildingsFromOsmFile(absoluteFileName, buildings)
        
    print("\r" + printPrefixString + "Loading files is done...                                              ")
    print(printPrefixString + "#buildings: " + str(len(buildings)))
    
    saveAllBuldingsGis(buildings, outputGISFile, printPrefixString)
    
    #print("#buildings: " + str(len(buildings)))

def saveAllBuldingsGis(buildings, fileName, printPrefixString = ""):
    
    print(printPrefixString + "Saving GIS information for builings to " + fileName + "...")
    
    # create output file
    output = open(fileName, 'w')
    output.write("id;category;polygon\n")
    
    for ID in buildings:
        building = buildings[ID]
        output.write(str(building.ID) + ";")
        output.write(building.category + ";")
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
