"""
This files contains functions to process traffic data.
"""

from rectangles import loadRectangles

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
    
    rectangles = []
    
    # load rectangles
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
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
        #LINESTRING (30 10, 10 30, 40 40)
        output.write("LINESTRING (" + str(roadData.longitude1) + " ")
        output.write(str(roadData.latitude1) + ", ")
        output.write(str(roadData.longitude2 + " "))
        output.write(str(roadData.latitude2 + ")\n"))
    
    output.close()
    
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Calculating roads for each rectangles...")
    
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