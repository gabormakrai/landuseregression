"""
Processing Automated Traffic Counter data
"""
from rectangles import loadRectangles
import os.path


def processAtcFile(year, atcData, stationId, fileName, printPrefixString):
    
    print(printPrefixString + "Processing file " + fileName)
    
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
            dateString = splittedLine[0]
            traffic = []
            for i in range(14,33):
                traffic.append(splittedLine[i])
            
            yearString = dateString[6:10]
            
            if str(year) != str(yearString):
                continue  
            
            monthString = dateString[3:5]
            dayString = dateString[0:2]
            
            dayTimestampKey = yearString + monthString + dayString
            
            for hour in range(0,24):
                try:
                    if hour < 6:
                        atc = float(traffic[0]) / 6.0
                    else:
                        atc = float(traffic[hour - 6])
                except ValueError:
                    continue
                
                if hour < 10:
                    timestampKey = dayTimestampKey + "0" + str(hour)
                else:
                    timestampKey = dayTimestampKey + str(hour)
                    
                if stationId not in atcData:
                    atcData[stationId] = {}
                
                if timestampKey not in atcData[stationId]:
                    atcData[stationId][timestampKey] = atc
                else:
                    precAtc = atcData[stationId][timestampKey]
                    atcData[stationId][timestampKey] = precAtc + atc
                

def processAtcData(year, inputRectangleFile, inputAtcDirectory, outputFile, printPrefixString = ""):
    
    atcData = {}
    
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    for rectangle in rectangles:
        stationName = str(rectangle.name.lower())
        atcFile1 = inputAtcDirectory + stationName + "1.csv"
        atcFile2 = inputAtcDirectory + stationName + "2.csv" 
        if os.path.isfile(atcFile1):
            processAtcFile(year, atcData, str(rectangle.ID), atcFile1, printPrefixString)
        if os.path.isfile(atcFile2):
            processAtcFile(year, atcData, str(rectangle.ID), atcFile2, printPrefixString)
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,atc\n")
    
    for stationId in atcData:
        for timestampKey in atcData[stationId]:
            output.write(stationId + "," + timestampKey + "," + str(atcData[stationId][timestampKey]) + "\n")

    output.close()
    
    