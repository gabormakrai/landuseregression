"""
This files contains functions to process traffic data.
"""

from rectangles import loadRectangles
from Geometry import linelineIntersection, pointInTriangle
from WGS84Coordinate import WGS84Coordinate
from MapCoordinate import MapCoordinate
from rtree import index

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

    # generate index
    print(printPrefixString + "Generating indicies for roadDatas...")
    indexedRoadDatas = generateIndex(roadDataArray)
    print(printPrefixString + "Done...")        
        
    #calculateRelatedRoadData(rectangles[2], roadDataArray)
    for rectangle in rectangles:
        print(printPrefixString + "\tstationId:" + str(rectangle.ID))
        
        rectangleRoadDataArray = []
                
        cornerSW = rectangle.cornerSW.toWGS84Coordinate()
        cornerNE = rectangle.cornerNE.toWGS84Coordinate()
        
        rectangleRoadDataList = list(indexedRoadDatas.intersection((cornerSW.longitude, cornerSW.latitude, cornerNE.longitude, cornerNE.latitude)))
        
        for r in rectangleRoadDataList:
            rectangleRoadDataArray.append(roadDataArray[r])
            
        calculateRelatedRoadData(rectangle, rectangleRoadDataArray)
    
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
    
    # write out gis File
    output = open(outputFile, 'w')
    
    #header
    output.write("location,tlc_am,tlc_ip,tlc_pm,tll_am,tll_ip,tll_pm,tlh_am,tlh_ip,tlh_pm,lane_length,length\n")
    
    for rectangle in rectangles:
        lane_length = 0
        length = 0
        
        for roadData in rectangle.roadDatas:
            c1 = MapCoordinate(roadData.c1.x, roadData.c1.y)
            c2 = MapCoordinate(roadData.c2.x, roadData.c2.y)
            roadLength = c1.toWGS84Coordinate().distance(c2)
            length = length + roadLength
            lane_length = lane_length + roadLength * float(roadData.laneNumber)
        
        traffic_length_car_am = 0
        traffic_length_lgv_am = 0
        traffic_length_hgv_am = 0
        
        traffic_length_car_ip = 0
        traffic_length_lgv_ip = 0
        traffic_length_hgv_ip = 0
        
        traffic_length_car_pm = 0
        traffic_length_lgv_pm = 0
        traffic_length_hgv_pm = 0
        
        for roadData in rectangle.roadDatas:
            c1 = MapCoordinate(roadData.c1.x, roadData.c1.y)
            c2 = MapCoordinate(roadData.c2.x, roadData.c2.y)
            roadLength = c1.toWGS84Coordinate().distance(c2)
            
            traffic_length_car_am = traffic_length_car_am + float(roadData.amCar) * roadLength
            traffic_length_lgv_am = traffic_length_lgv_am + float(roadData.amLgv) * roadLength
            traffic_length_hgv_am = traffic_length_hgv_am + float(roadData.amHgv) * roadLength
            
            traffic_length_car_ip = traffic_length_car_ip + float(roadData.ipCar) * roadLength
            traffic_length_lgv_ip = traffic_length_lgv_ip + float(roadData.ipLgv) * roadLength
            traffic_length_hgv_ip = traffic_length_hgv_ip + float(roadData.ipHgv) * roadLength

            traffic_length_car_pm = traffic_length_car_pm + float(roadData.pmCar) * roadLength
            traffic_length_lgv_pm = traffic_length_lgv_pm + float(roadData.pmLgv) * roadLength
            traffic_length_hgv_pm = traffic_length_hgv_pm + float(roadData.pmHgv) * roadLength
                 
        output.write(str(rectangle.ID) + ",")
        
        output.write(str(traffic_length_car_am) + ",")
        output.write(str(traffic_length_lgv_am) + ",")
        output.write(str(traffic_length_hgv_am) + ",")
        
        output.write(str(traffic_length_car_ip) + ",")
        output.write(str(traffic_length_lgv_ip) + ",")
        output.write(str(traffic_length_hgv_ip) + ",")
        
        output.write(str(traffic_length_car_pm) + ",")
        output.write(str(traffic_length_lgv_pm) + ",")
        output.write(str(traffic_length_hgv_pm) + ",")
            
        output.write(str(lane_length) + ",")
        output.write(str(length) + "\n")
    
    output.close()
    
    print(printPrefixString + "Done...")

def createRectangleTrafficAnnual(inputTrafficFile, inputRectangleFile, outputFile, outputGISFile, printPrefixString = ""):
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
        
    # generate index
    print(printPrefixString + "Generating indicies for roadDatas...")
    indexedRoadDatas = generateIndex(roadDataArray)
    print(printPrefixString + "Done...")        
        
    #calculateRelatedRoadData(rectangles[2], roadDataArray)
    for rectangle in rectangles:
        print(printPrefixString + "\tstationId:" + str(rectangle.ID))
        calculateRelatedRoadData(rectangle, roadDataArray, indexedRoadDatas)
    
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
    
    createTrafficRelatedDataAnnual(rectangles, outputFile, printPrefixString)
    
    
def createTrafficRelatedDataAnnual(rectangles, outputFile, printPrefixString = ""):
    print(printPrefixString + "Write out traffic related data to " + outputFile + "...")
    
    # write out gis File
    output = open(outputFile, 'w')
    
    #header
    output.write("location,traffic_length_car,traffic_length_lgv,traffic_length_hgv,lane_length,length\n")
    
    for rectangle in rectangles:
        lane_length = 0
        length = 0
        
        traffic_length_car = 0
        traffic_length_lgv = 0
        traffic_length_hgv = 0
        
        for roadData in rectangle.roadDatas:
            c1 = MapCoordinate(roadData.c1.x, roadData.c1.y)
            c2 = MapCoordinate(roadData.c2.x, roadData.c2.y)
            roadLength = c1.toWGS84Coordinate().distance(c2)
            length = length + roadLength
            lane_length = lane_length + roadLength * float(roadData.laneNumber)
            
            traffic_car = float(roadData.amCar) + float(roadData.ipCar) + float(roadData.pmCar)
            traffic_lgv = float(roadData.amLgv) + float(roadData.ipLgv) + float(roadData.pmLgv)
            traffic_hgv = float(roadData.amHgv) + float(roadData.ipHgv) + float(roadData.pmHgv)
            
            traffic_length_car = traffic_length_car + traffic_car * roadLength
            traffic_length_lgv = traffic_length_lgv + traffic_lgv * roadLength
            traffic_length_hgv = traffic_length_hgv + traffic_hgv * roadLength
       
        output.write(str(rectangle.ID) + ",")
        output.write(str(traffic_length_car) + ",")
        output.write(str(traffic_length_lgv) + ",")
        output.write(str(traffic_length_hgv) + ",")
        output.write(str(lane_length) + ",")
        output.write(str(length) + "\n")
    
    output.close()
    
    print(printPrefixString + "Done...")    

def generateIndex(roadDataArray):
    idx = index.Index()
    
    for i in range(0, len(roadDataArray)):
        roadData = roadDataArray[i]
        
        c1 = roadData.c1.toWGS84Coordinate()
        c2 = roadData.c2.toWGS84Coordinate()
        
        minLat = c1.latitude
        minLon = c1.longitude
        maxLat = c1.latitude
        maxLon = c1.longitude
        
        if (c2.latitude > maxLat):
            maxLat = c2.latitude
        if (c2.latitude < minLat):
            minLat = c2.latitude
        if (c2.longitude > maxLon):
            maxLon = c2.longitude
        if (c2.longitude < minLon):
            minLon = c2.longitude
            
        idx.add(i, (minLon, minLat, maxLon, maxLat))
    
    return idx

def addTimestampToTraffic(timestamps, inputFile, outputFile, printPrefixString = ""):
    
    data = {}
    
    print(printPrefixString + "Loading traffic data from " + inputFile + " file...")
    
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
            
            location = splittedLine[0]
            
            trafficData = {}
            
            trafficData["tlc_am"] = splittedLine[1]
            trafficData["tll_am"] = splittedLine[2]
            trafficData["tlh_am"] = splittedLine[3]
            
            trafficData["tlc_ip"] = splittedLine[4]
            trafficData["tll_ip"] = splittedLine[5]
            trafficData["tlh_ip"] = splittedLine[6]
            
            trafficData["tlc_pm"] = splittedLine[7]
            trafficData["tll_pm"] = splittedLine[8]
            trafficData["tlh_pm"] = splittedLine[9]
            
            trafficData["lane_length"] = splittedLine[10]
            trafficData["length"] = splittedLine[11]
            
            data[location] = trafficData
            
    print(printPrefixString + "Done...")     
    
    print(printPrefixString + "Writing out data with timestamps to traffic data " + outputFile + "...")
    
    # write out gis File
    output = open(outputFile, 'w')
    
    output.write("location,timestamp,traffic_length_car,traffic_length_lgv,traffic_length_hgv,lane_length,length\n")
    
    for location in data:
        for timestamp in timestamps:
            traffic_length_car = 0.0
            traffic_length_lgv = 0.0
            traffic_length_hgv = 0.0
            
            if timestamp.hour < 8:
                traffic_length_car = float(data[location]['tlc_am']) / 4.0 
                traffic_length_lgv = float(data[location]['tll_am']) / 4.0 
                traffic_length_hgv = float(data[location]['tlh_am']) / 4.0 
            elif timestamp.hour >= 8 and timestamp.hour < 10:
                traffic_length_car = float(data[location]['tlc_am'])
                traffic_length_lgv = float(data[location]['tll_am'])
                traffic_length_hgv = float(data[location]['tlh_am'])
            elif timestamp.hour >= 10 and timestamp.hour < 17:
                traffic_length_car = float(data[location]['tlc_ip'])
                traffic_length_lgv = float(data[location]['tll_ip'])
                traffic_length_hgv = float(data[location]['tlh_ip'])
            elif timestamp.hour >= 17 and timestamp.hour < 19:
                traffic_length_car = float(data[location]['tlc_pm'])
                traffic_length_lgv = float(data[location]['tll_pm'])
                traffic_length_hgv = float(data[location]['tlh_pm'])
            else:
                traffic_length_car = float(data[location]['tlc_pm']) / 4.0
                traffic_length_lgv = float(data[location]['tll_pm']) / 4.0
                traffic_length_hgv = float(data[location]['tlh_pm']) / 4.0
    
            output.write(location + ",")
            output.write(timestamp.key + ",")
            output.write(str(traffic_length_car) + ",")
            output.write(str(traffic_length_lgv) + ",")
            output.write(str(traffic_length_hgv) + ",")
            output.write(data[location]['lane_length'] + ",")
            output.write(data[location]['length'] + "\n")
            
    output.close()
