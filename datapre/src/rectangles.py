"""
This file contains functions for creating rectangles (for stations and for
whole areas)
"""

from MapCoordinate import MapCoordinate
from WGS84Coordinate import WGS84Coordinate

class Rectangle:
    def __init__(self, ID, name, cornerNW, cornerNE, cornerSE, cornerSW):
        self.ID = ID
        self.name = name
        self.cornerNW = cornerNW
        self.cornerNE = cornerNE
        self.cornerSE = cornerSE
        self.cornerSW = cornerSW

class Station:
    def __init__(self, ID, name, latitude, longitude):
        self.ID = ID
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
    def toString(self):
        return "Station(id:" + str(self.ID) + ",name:" + str(self.name) + ",lat:" + str(self.latitude) + "lng:" + str(self.longitude) + ")"


"""
Generate rectangles for a specific grid...
"""
def generateGridStationRectangles(rectangleSize, latitudeNW, longitudeNW, latitudeSE, longitudeSE, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "Generating rectangles for the grid...")
    
    stations = []
    
#     distanceLatitude = 0.0
#     distanceLongitude = 0.0
    
    c1 = WGS84Coordinate(latitudeNW, longitudeNW)
    c2 = WGS84Coordinate(latitudeSE, longitudeNW)
    c3 = WGS84Coordinate(latitudeNW, longitudeSE)
    
    distanceLatitude = c1.distance(c2)
    distanceLongitude = c1.distance(c3)
    
    minLatitude = latitudeNW
    minLongitude = longitudeNW
    
    gridX = int(distanceLongitude / rectangleSize)
    gridY = int(distanceLatitude / rectangleSize)
    
    dLatitude = (rectangleSize / distanceLatitude) * (latitudeSE - latitudeNW)
    dLongitude = (rectangleSize / distanceLongitude) * (longitudeSE - longitudeNW)
    
#     maxLatitude = minLatitude + (gridY + 1) * dLatitude
#     maxLongitude = minLongitude + (gridX + 1) * dLongitude
    
    ID = 0
    
    for y in range(0, gridY): 
        for x in range(0, gridX):
            name = "grid" + str(ID)
            ID = ID + 1
            lat1 = minLatitude + (y + 0) * dLatitude
            lat2 = minLatitude + (y + 1) * dLatitude
            long1 = minLongitude + (x + 0) * dLongitude
            long2 = minLongitude + (x + 1) * dLongitude
            
            lat3 = (lat1 + lat2) / 2.0
            long3 = (long1 + long2) / 2.0
            
            station = Station(ID, name, lat3, long3)
            
            station.northWestCorner = WGS84Coordinate(lat1, long1)
            station.northEastCorner = WGS84Coordinate(lat1, long2)
            station.southWestCorner = WGS84Coordinate(lat2, long1)
            station.southEastCorner = WGS84Coordinate(lat2, long2)
            
            stations.append(station)
            
    print(printPrefixString + "\t#stations: " + str(len(stations)))
    
    print(printPrefixString + "Saving rectangles to " + outputFile + "...")
    
    # create output file
    output = open(outputFile, 'w')
    output.write("id,name,nw_latitude,nw_longitude,ne_latitude,ne_longitude,se_latitude,se_longitude,sw_latitude,sw_longitude\n")
    
    for station in stations:
        output.write(str(station.ID) + ",")
        output.write(str(station.name) + ",")
        output.write(str(station.northWestCorner.latitude) + ",")
        output.write(str(station.northWestCorner.longitude) + ",")
        output.write(str(station.northEastCorner.latitude) + ",")
        output.write(str(station.northEastCorner.longitude) + ",")
        output.write(str(station.southEastCorner.latitude) + ",")
        output.write(str(station.southEastCorner.longitude) + ",")
        output.write(str(station.southWestCorner.latitude) + ",")
        output.write(str(station.southWestCorner.longitude) + "\n")
        
    output.close()
    
    print(printPrefixString + "Done...")
    
                
"""
This function is creating buffer rectangles for each air quality monitoring
station. 
The input file should contains a header line and the following columns in order:
id,name,latitude,longitude
"""

def createStationRectangles(rectangleSize, stationFile, outputFile, outputGISFile, printPrefixString = ""):

    stations = []
    
    print(printPrefixString + "Loading " + stationFile + " station file...")
    
    firstLine = True
    # open the file
    with open(stationFile) as infile:
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
            
    print(printPrefixString + "#stations: " + str(len(stations)))
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Do the corner calculation...")
    
    # function that calculates the buffer rectangle corners
    def addCorners(station):
        coordinate = WGS84Coordinate(station.latitude, station.longitude)
        delta = 0.0001
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
    
    print(printPrefixString + "Done...")
    
    saveRectangles(stations, outputFile, printPrefixString)
    
    # create gis outputfile
    print(printPrefixString + "Saving down GIS information to " + outputGISFile + "...")
    
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
    
    print(printPrefixString + "Done...")

def saveRectangles(stations, outputFile, printPrefixString = ""):
    print(printPrefixString + "Saving rectangles to " + outputFile + "...")
    
    # create output file
    output = open(outputFile, 'w')
    output.write("id,name,nw_latitude,nw_longitude,ne_latitude,ne_longitude,se_latitude,se_longitude,sw_latitude,sw_longitude\n")
    
    for station in stations:
        output.write(str(station.ID) + ",")
        output.write(str(station.name) + ",")
        output.write(str(station.northWestCorner.latitude) + ",")
        output.write(str(station.northWestCorner.longitude) + ",")
        output.write(str(station.northEastCorner.latitude) + ",")
        output.write(str(station.northEastCorner.longitude) + ",")
        output.write(str(station.southEastCorner.latitude) + ",")
        output.write(str(station.southEastCorner.longitude) + ",")
        output.write(str(station.southWestCorner.latitude) + ",")
        output.write(str(station.southWestCorner.longitude) + "\n")
        
    output.close()
    
    print(printPrefixString + "Done...")


def loadRectangles(rectangles, inputRectangleFile, printPrefixString = ""):
    print(printPrefixString + "Loading " + inputRectangleFile + " rectangle file...")
    
    firstLine = True
    # open the file
    with open(inputRectangleFile) as infile:
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
            #id,nw_latitude,nw_longitude,ne_latitude,ne_longitude,se_latitude,se_longitude,sw_latitude,sw_longitude
            northWestCoordinate = WGS84Coordinate(float(splittedLine[2]), float(splittedLine[3])).toMapCoordinate()
            northEastCoordinate = WGS84Coordinate(float(splittedLine[4]), float(splittedLine[5])).toMapCoordinate()
            southEastCoordinate = WGS84Coordinate(float(splittedLine[6]), float(splittedLine[7])).toMapCoordinate()
            southWestCoordinate = WGS84Coordinate(float(splittedLine[8]), float(splittedLine[9])).toMapCoordinate()
            rectangle = Rectangle(splittedLine[0], splittedLine[1], northWestCoordinate, northEastCoordinate, southEastCoordinate, southWestCoordinate)
            rectangles.append(rectangle)
    
    print(printPrefixString + "#rectangles: " + str(len(rectangles)))
    print(printPrefixString + "Done...")

def createJsonFile(rectangleFile, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "loading rectangles from file " + rectangleFile + "...")
    
    rectangles = []
    loadRectangles(rectangles, rectangleFile, printPrefixString + "\t") 
    
    print(printPrefixString + "done...")
    
    print(printPrefixString + "create json file and write it to " + outputFile + "...")
    
    # create output file
    output = open(outputFile, 'w')
    output.write('{ "cells": [\n');
    
    firstRecord = True
    
    for station in rectangles:
        
        if firstRecord == True:
            firstRecord = False
        else:
            output.write(",\n")
        
#         output.write("{")
#         output.write('"id": ' + str(station.ID) + ",")
#         output.write('"c1": {"latitude":')
#         output.write(str(station.cornerNW.toWGS84Coordinate().latitude)[0:7] + ",")
#         output.write('"longitude":')
#         output.write(str(station.cornerNW.toWGS84Coordinate().longitude)[0:7] + "},")
#         
#         output.write('"c2": {"latitude":')
#         output.write(str(station.cornerNE.toWGS84Coordinate().latitude)[0:7] + ",")
#         output.write('"longitude":')
#         output.write(str(station.cornerNE.toWGS84Coordinate().longitude)[0:7] + "},")
#         
#         output.write('"c3": {"latitude":')
#         output.write(str(station.cornerSE.toWGS84Coordinate().latitude)[0:7] + ",")
#         output.write('"longitude":')
#         output.write(str(station.cornerSE.toWGS84Coordinate().longitude)[0:7] + "},")
#         
#         output.write('"c4": {"latitude":')
#         output.write(str(station.cornerSW.toWGS84Coordinate().latitude)[0:7] + ",")
#         output.write('"longitude":')
#         output.write(str(station.cornerSW.toWGS84Coordinate().longitude)[0:7] + "}}")

        output.write("[")
        output.write(str(station.ID) + ",")
        output.write(str(station.cornerNW.toWGS84Coordinate().latitude)[0:7] + ",")
        output.write(str(station.cornerNW.toWGS84Coordinate().longitude)[0:7] + ",")
        output.write(str(station.cornerNE.toWGS84Coordinate().latitude)[0:7] + ",")
        output.write(str(station.cornerNE.toWGS84Coordinate().longitude)[0:7] + ",")
        output.write(str(station.cornerSE.toWGS84Coordinate().latitude)[0:7] + ",")
        output.write(str(station.cornerSE.toWGS84Coordinate().longitude)[0:7] + ",")
        output.write(str(station.cornerSW.toWGS84Coordinate().latitude)[0:7] + ",")
        output.write(str(station.cornerSW.toWGS84Coordinate().longitude)[0:7] )
        output.write("]")
        
    output.write(']}\n');
    output.close()
    
    print(printPrefixString + "done...")
    