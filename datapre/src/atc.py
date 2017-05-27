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
    
def general_stats_about_london_atc(fileName, printPrefixString):
    
    print(printPrefixString + "Parsing atc file " + str(fileName) + " and generating stats...")

    station_ids = set()
    data_counter = {}
    
    firstLine = True    
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
            station = splittedLine[0]
            station_ids.add(station)
            if station not in data_counter:
                data_counter[station] = 0
            data_counter[station] = data_counter[station] + 1
    print(printPrefixString + "\t#Stations:" + str(len(station_ids)))
    for station in data_counter:
        print(printPrefixString + "\t" + str(station) + ": " + str(data_counter[station]))
    print(printPrefixString + "Done...")

def process_london_atc_data(atcFile, atcSiteFile, outputFile, printPrefixString = ""):
    
    atcData = {}
    monthsStrings = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}

    print(printPrefixString + "Parsing atc file " + str(atcFile) + " for atc data...")
    
    firstLine = True
    siteNoColumn = -1
    dateColumn = -1
    startHourColumn = -1
    totVolColumn = -1    
    with open(atcFile) as infile:
        # read line by line
        for line in infile:
            # remove newline character from the end
            line = line.rstrip()
            # split the line
            splittedLine = line.split(',')
            # skip the first line (header line)
            if firstLine == True:
                for i in range(0, len(splittedLine)):
                    if splittedLine[i] == 'SiteNo':
                        siteNoColumn = i
                    if splittedLine[i] == 'Date':
                        dateColumn = i
                    if splittedLine[i] == 'Starthour':
                        startHourColumn = i
                    if splittedLine[i] == 'TOT Vol':
                        totVolColumn = i
                firstLine = False
                continue
            station = splittedLine[siteNoColumn]
            dateString = splittedLine[dateColumn]
            hour = int(splittedLine[startHourColumn]) + 1
            hourString = str(hour)
            if hour < 10:
                hourString = "0" + hourString
            counter = float(splittedLine[totVolColumn])

            if len(dateString) == 9:            
                dayString = dateString[0:2]
                monthString = monthsStrings[dateString[3:6].upper()]
                yearString = "20" + dateString[7:]
            else:
                #1/1/2016 00:00:00
                dayString = dateString.split(" ")[0].split("/")[0]
                if len(dayString) == 1: dayString = "0" + dayString
                monthString = dateString.split(" ")[0].split("/")[1]
                if len(monthString) == 1: monthString = "0" + monthString
                yearString = dateString.split(" ")[0].split("/")[2]
                
            timestampString = yearString + monthString + dayString + hourString
            if station not in atcData:
                atcData[station] = {}
            
            if timestampString in atcData[station]:
                atcData[station][timestampString] = (atcData[station][timestampString] + counter) / 2.0
            else:
                atcData[station][timestampString] = counter
    
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Parsing atc site file " + atcSiteFile + " for site matching...")
    
    stationAtcData = {}
    
    firstLine = True    
    with open(atcSiteFile) as infile:
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
            
            monitoringSite = splittedLine[0]
            stationAtcData[monitoringSite] = {}
            atc1Site = splittedLine[1]
            atc2Site = splittedLine[2]
            
            if atc2Site != '-1':
                atc1Data = {}
                if atc1Site in atcData:
                    atc1Data = atcData[atc1Site]
                atc2Data = {}
                if atc2Site in atcData:
                    atc2Data = atcData[atc2Site]
                
                timestamps = set()
                for ts in atc1Data: timestamps.add(ts) 
                for ts in atc2Data: timestamps.add(ts)
                
                for ts in timestamps:
                    atc1 = 0.0
                    atc2 = 0.0
                    counter = 0
                    if ts in atc1Data:
                        atc1 = atc1Data[ts] 
                        counter = counter + 1
                    if ts in atc2Data:
                        atc2 = atc2Data[ts] 
                        counter = counter + 1
                    atc = (atc1 + atc2) / counter
                    
                    stationAtcData[monitoringSite][ts] = atc
            else:
                atc1Data = {}
                if atc1Site in atcData:
                    atc1Data = atcData[atc1Site]
                stationAtcData[monitoringSite] = atc1Data
    print(printPrefixString + "Done...")
    
    print(printPrefixString + "Writing out atc data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,atc\n")
    
    for station in stationAtcData:
        for ts in stationAtcData[station]:
            output.write(station + "," + ts + "," + str(stationAtcData[station][ts]) + "\n")

    output.close()        
    print(printPrefixString + "Done...")