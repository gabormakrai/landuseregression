"""
This files contains functions to process traffic data.
"""

from rectangles import loadRectangles
from Geometry import linelineIntersection, pointInTriangle
from WGS84Coordinate import WGS84Coordinate
from MapCoordinate import MapCoordinate
from Timestamp import generateTimestamps

class RoadData:
    def __init__(self, ID, longitude1, latitude1, longitude2, latitude2, speedLimit, laneNumber, oneWay, amCar, amLgv, amHgv, ipCar, ipLgv, ipHgv, pmCar, pmLgv, pmHgv):
        self.ID = ID
        self.longitude1 = float(longitude1)
        self.latitude1 = float(latitude1)
        self.longitude2 = float(longitude2)
        self.latitude2 = float(latitude2)
        self.speedLimit = speedLimit
        self.laneNumber = laneNumber
        self.oneWay = oneWay
        self.amCar = amCar
        self.amLgv = amLgv
        self.amHgv = amHgv
        self.ipCar = ipCar
        self.ipLgv = ipLgv
        self.ipHgv = ipHgv
        self.pmCar = pmCar
        self.pmLgv = pmLgv
        self.pmHgv = pmHgv
    def copy(self):
        return RoadData(self.ID, self.longitude1, self.latitude1, self.longitude2, self.latitude2, self.speedLimit, self.laneNumber, self.oneWay, self.amCar, self.amLgv, self.amHgv, self.ipCar, self.ipLgv, self.ipHgv, self.pmCar, self.pmLgv, self.pmHgv)
        
"""
This function is creating gis file for analyzing all the traffic.
The input traffic file should contains a header line and the following columns in order:
id,longitude1,latitude1,longitude2,latitude2,speed_limit,lane_number,one_way,am_car,am_lgv,am_hgv,ip_car,ip_lgv,ip_hgv,pm_car,pm_lgv,pm_hgv
The input rectangle file should contain the rectangle informations
"""
def createTrafficGISFile(inputRectangleFile, inputTrafficFile, outputGISFile, printPrefixString = ""):
        
    roadDataArray = []
    
    # load the data
    loadTraffic(roadDataArray, inputTrafficFile, printPrefixString)
        
    print(printPrefixString + "write all traffic information to " + outputGISFile + "...")
    # write out gis File
    output = open(outputGISFile, 'w')
    
    #header
    output.write("id;speed_limit;lane_number;one_way;am_car;am_lgv;am_hgv;ip_car;ip_lgv;ip_hgv;pm_car;pm_lgv;pm_hgv;linestring\n")
    
    for roadData in roadDataArray:
        output.write(str(roadData.ID) + ";")
        output.write(str(roadData.speedLimit) + ";")
        output.write(str(roadData.laneNumber) + ";")
        output.write(str(roadData.oneWay) + ";")
        output.write(str(roadData.amCar) + ";")
        output.write(str(roadData.amLgv) + ";")
        output.write(str(roadData.amHgv) + ";")
        output.write(str(roadData.ipCar) + ";")
        output.write(str(roadData.ipLgv) + ";")
        output.write(str(roadData.ipHgv) + ";")
        output.write(str(roadData.pmCar) + ";")
        output.write(str(roadData.pmLgv) + ";")
        output.write(str(roadData.pmHgv) + ";")
        output.write("LINESTRING (" + str(roadData.longitude1) + " ")
        output.write(str(roadData.latitude1) + ", ")
        output.write(str(roadData.longitude2) + " ")
        output.write(str(roadData.latitude2) + ")\n")
    
    output.close()
    
    print(printPrefixString + "Done...")

def loadTraffic(roadDataArray, inputTrafficFile, printPrefixString = ""):
    
    print(printPrefixString + "Loading " + inputTrafficFile + " traffic file...")
    
    firstLine = True
    # open the file
    with open(inputTrafficFile) as infile:
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
            roadData = RoadData(splittedLine[0], splittedLine[1], splittedLine[2],
                splittedLine[3], splittedLine[4], splittedLine[5], splittedLine[6],
                splittedLine[7], splittedLine[8], splittedLine[9], splittedLine[10],
                splittedLine[11], splittedLine[12], splittedLine[13], splittedLine[14],
                splittedLine[15], splittedLine[16])
            roadDataArray.append(roadData)
            
    print(printPrefixString + "#roadData: " + str(len(roadDataArray)))
    print(printPrefixString + "Done...")    

def createRectangleTraffic(inputTrafficFile, inputRectangleFile, outputFile, outputGISFile, printPrefixString = ""):
    roadDataArray = []
    # load traffic data
    loadTraffic(roadDataArray, inputTrafficFile, printPrefixString)
    
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)

    print(printPrefixString + "Calculate RoadDatas for each rectangle...")
    
    # add MapCoordinates for roadDataArray
    for roadData in roadDataArray:
        roadData.c1 = WGS84Coordinate(roadData.latitude1, roadData.longitude1).toMapCoordinate()
        roadData.c2 = WGS84Coordinate(roadData.latitude2, roadData.longitude2).toMapCoordinate()
        
    #calculateRelatedRoadData(rectangles[2], roadDataArray)
    for rectangle in rectangles:
        print(printPrefixString + "\tstationId:" + str(rectangle.ID))
        calculateRelatedRoadData(rectangle, roadDataArray)
    
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Collect all the roadData which is part of the rectangles...")

    rectanglesRoadDataArray = []
    for rectangle in rectangles:
        for roadData in rectangle.roadDatas:
            rectanglesRoadDataArray.append(roadData)
            
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Write out rectangle roadData GIS information to " + outputGISFile + "...")
    
    # write out gis File
    output = open(outputGISFile, 'w')
    
    #header
    output.write("id;speed_limit;lane_number;one_way;am_car;am_lgv;am_hgv;ip_car;ip_lgv;ip_hgv;pm_car;pm_lgv;pm_hgv;linestring\n")
    
    for roadData in rectanglesRoadDataArray:
        output.write(str(roadData.ID) + ";")
        output.write(str(roadData.speedLimit) + ";")
        output.write(str(roadData.laneNumber) + ";")
        output.write(str(roadData.oneWay) + ";")
        output.write(str(roadData.amCar) + ";")
        output.write(str(roadData.amLgv) + ";")
        output.write(str(roadData.amHgv) + ";")
        output.write(str(roadData.ipCar) + ";")
        output.write(str(roadData.ipLgv) + ";")
        output.write(str(roadData.ipHgv) + ";")
        output.write(str(roadData.pmCar) + ";")
        output.write(str(roadData.pmLgv) + ";")
        output.write(str(roadData.pmHgv) + ";")
        c1 = MapCoordinate(roadData.c1.x, roadData.c1.y).toWGS84Coordinate()
        c2 = MapCoordinate(roadData.c2.x, roadData.c2.y).toWGS84Coordinate()
        output.write("LINESTRING (" + str(c1.longitude) + " ")
        output.write(str(c1.latitude) + ", ")
        output.write(str(c2.longitude) + " ")
        output.write(str(c2.latitude) + ")\n")
    
    output.close()
    
    print(printPrefixString + "Done...")
    
    createTrafficRelatedData(rectangles, outputFile, printPrefixString)

"""
Function that finds all the roadData for a rectangle
"""
def calculateRelatedRoadData(rectangle, roadDataArray):
    
    updatedRoadDataArray = []
    
    # rectangle sides
    sideNorth1 = rectangle.cornerNW.toMapCoordinate()
    sideNorth2 = rectangle.cornerNE.toMapCoordinate()
    sideEast1 = rectangle.cornerNE.toMapCoordinate()
    sideEast2 = rectangle.cornerSE.toMapCoordinate()
    sideSouth1 = rectangle.cornerSE.toMapCoordinate()
    sideSouth2 = rectangle.cornerSW.toMapCoordinate()
    sideWest1 = rectangle.cornerSW.toMapCoordinate()
    sideWest2 = rectangle.cornerNW.toMapCoordinate()
    
    # for each roaddata, lets find out that the sides of the rectangle
    # is crossing the roaddata or not
    # if yes, then cut the roadData into two parts
    
    for roadData in roadDataArray:
        
        intersectionNorth = linelineIntersection(sideNorth1, sideNorth2, roadData.c1, roadData.c2)
        intersectionSouth = linelineIntersection(sideSouth1, sideSouth2, roadData.c1, roadData.c2)
        intersectionWest = linelineIntersection(sideWest1, sideWest2, roadData.c1, roadData.c2)
        intersectionEast = linelineIntersection(sideEast1, sideEast2, roadData.c1, roadData.c2)
        
        intersections = []
    
        if intersectionNorth != None:
            intersections.append(intersectionNorth)
        if intersectionSouth != None:
            intersections.append(intersectionSouth)
        if intersectionWest != None:
            intersections.append(intersectionWest)
        if intersectionEast != None:
            intersections.append(intersectionEast)
            
        if len(intersections) == 0:
            updatedRoadDataArray.append(roadData)
        elif len(intersections) == 1:
            rd1 = roadData.copy()
            rd2 = roadData.copy()
            rd1.c1 = WGS84Coordinate(roadData.latitude1, roadData.longitude1).toMapCoordinate()
            rd1.c2 = intersections[0]
            rd2.c1 = intersections[0]
            rd2.c2 = WGS84Coordinate(roadData.latitude2, roadData.longitude2).toMapCoordinate()
            updatedRoadDataArray.append(rd1)
            updatedRoadDataArray.append(rd2)
        elif len(intersections) == 2:
            rd1 = roadData.copy()
            rd1.c1 = intersections[0]
            rd1.c2 = intersections[1]
            updatedRoadDataArray.append(rd1)
                        
    # calculate the middle point of each roadData
    for roadData in updatedRoadDataArray:
        cx = (roadData.c1.x + roadData.c2.x) / 2.0
        cy = (roadData.c1.y + roadData.c2.y) / 2.0
        roadData.cc = MapCoordinate(cx, cy)
    
    # find out which middlepoint is in the rectangle
    rectangleRoadData = []
    for roadData in updatedRoadDataArray:
        a = pointInTriangle(rectangle.cornerNW, rectangle.cornerNE, rectangle.cornerSE, roadData.cc)
        b = pointInTriangle(rectangle.cornerNW, rectangle.cornerSE, rectangle.cornerSW, roadData.cc)
        if a == True or b == True:
            rectangleRoadData.append(roadData)
    
    rectangle.roadDatas = rectangleRoadData
    
def createTrafficRelatedData(rectangles, outputFile, printPrefixString = ""):
    print(printPrefixString + "Write out traffic related data to " + outputFile + "...")

    # generate all timestamps    
    timestamps = generateTimestamps(2013)
    
    # write out gis File
    output = open(outputFile, 'w')
    
    #header
    output.write("location,timestamp,traffic_length_car,traffic_length_lgv,traffic_length_hgv,lane_length,length\n")
    
    for rectangle in rectangles:
        lane_length = 0
        length = 0
        
        for roadData in rectangle.roadDatas:
            c1 = MapCoordinate(roadData.c1.x, roadData.c1.y)
            c2 = MapCoordinate(roadData.c2.x, roadData.c2.y)
            roadLength = c1.toWGS84Coordinate().distance(c2)
            length = length + roadLength
            lane_length = lane_length + roadLength * float(roadData.laneNumber)
        
        for timestamp in timestamps:
            traffic_length_car = 0
            traffic_length_lgv = 0
            traffic_length_hgv = 0
            for roadData in rectangle.roadDatas:
                c1 = MapCoordinate(roadData.c1.x, roadData.c1.y)
                c2 = MapCoordinate(roadData.c2.x, roadData.c2.y)
                roadLength = c1.toWGS84Coordinate().distance(c2)
                traffic_car = 0
                traffic_lgv = 0
                traffic_hgv = 0
                if timestamp.hour < 8:
                    traffic_car = float(roadData.amCar) / 4.0
                    traffic_lgv = float(roadData.amLgv) / 4.0
                    traffic_hgv = float(roadData.amHgv) / 4.0
                elif timestamp.hour >= 8 and timestamp.hour < 10:
                    traffic_car = float(roadData.amCar)
                    traffic_lgv = float(roadData.amLgv)
                    traffic_hgv = float(roadData.amHgv)
                elif timestamp.hour >= 10 and timestamp.hour < 17:
                    traffic_car = float(roadData.ipCar)
                    traffic_lgv = float(roadData.ipLgv)
                    traffic_hgv = float(roadData.ipHgv)
                elif timestamp.hour >= 17 and timestamp.hour < 18:
                    traffic_car = float(roadData.pmCar)
                    traffic_lgv = float(roadData.pmLgv)
                    traffic_hgv = float(roadData.pmHgv)
                else:
                    traffic_car = float(roadData.pmCar) / 4.0
                    traffic_lgv = float(roadData.pmLgv) / 4.0
                    traffic_hgv = float(roadData.pmHgv) / 4.0
                
                traffic_length_car = traffic_length_car + traffic_car * roadLength
                traffic_length_lgv = traffic_length_lgv + traffic_lgv * roadLength
                traffic_length_hgv = traffic_length_hgv + traffic_hgv * roadLength
                 
            output.write(str(rectangle.ID) + "," + str(timestamp.key) + ",")
            output.write(str(traffic_length_car) + ",")
            output.write(str(traffic_length_lgv) + ",")
            output.write(str(traffic_length_hgv) + ",")
                
            output.write(str(lane_length) + ",")
            output.write(str(length) + "\n")
    
    output.close()
    
    print(printPrefixString + "Done...")
