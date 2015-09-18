"""
This script is calculating traffic related features for rectangles.
It also creates gis files for analyzing the input data.
It loads the file DATA_DIRECTORY/traffic/traffic.csv and creates the file
DATA_DIRECTORY/preprocessed/rectangles_traffic.csv
The input file should contains a header line and the following columns in order:
id,longitude1,latitude1,longitude2,latitude2,speed_limit,lane_number,one_way,am_car,am_lgv,am_hgv,ip_car,ip_lgv,ip_hgv,pm_car,pm_lgv,pm_hgv
"""
from directories import DATA_DIRECTORY
from WGS84Coordinate import WGS84Coordinate

class Rectangle:
    def __init__(self, ID, conerNW, cornerNE, cornerSE, cornerSW):
        self.ID = ID
        self.cornerNW = conerNW
        self.cornerNE = cornerNE
        self.cornerSE = cornerSE
        self.cornerSW = cornerSW

class RoadData:
    def __init__(self, ID, longitude1, latitude1, longitude2, latitude2, speedLimit, laneNumber, oneWay, amCar, amLgv, amHgv, ipCar, ipLgv, ipHgv, pmCar, pmLgv, pmHgv):
        self.ID = ID
        self.longitude1 = longitude1
        self.latitude1 = latitude1
        self.longitude2 = longitude2
        self.latitude2 = latitude2
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

inputTrafficFile = DATA_DIRECTORY + "traffic/traffic.csv"
inputRectangleFile = DATA_DIRECTORY + "stations/stations_rectangles.csv"
outputFile = DATA_DIRECTORY + "preprocessed/rectangles_traffic.csv"
outputGISFile = DATA_DIRECTORY + "gis/stations_rectangles_traffic.csv"
        
roadDataArray = []
# load the data

print("Loading " + inputTrafficFile + " traffic file...")

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
        
print("#roadData: " + str(len(roadDataArray)))
print("Done...")

rectangles = []

print("Loading " + inputRectangleFile + " rectangle file...")

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
        northWestCoordinate = WGS84Coordinate(float(splittedLine[1]), float(splittedLine[2])).toMapCoordinate()
        northEastCoordinate = WGS84Coordinate(float(splittedLine[3]), float(splittedLine[4])).toMapCoordinate()
        southEastCoordinate = WGS84Coordinate(float(splittedLine[5]), float(splittedLine[6])).toMapCoordinate()
        southWestCoordinate = WGS84Coordinate(float(splittedLine[7]), float(splittedLine[8])).toMapCoordinate()
        rectangle = Rectangle(splittedLine[0], northWestCoordinate, northEastCoordinate, southEastCoordinate, southWestCoordinate)
        rectangles.append(rectangle)

print("#rectangles: " + str(len(rectangles)))
print("Done...")

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
    #LINESTRING (30 10, 10 30, 40 40)
    output.write("LINESTRING (" + str(roadData.longitude1) + " ")
    output.write(str(roadData.latitude1) + ", ")
    output.write(str(roadData.longitude2 + " "))
    output.write(str(roadData.latitude2 + ")\n"))

output.close()