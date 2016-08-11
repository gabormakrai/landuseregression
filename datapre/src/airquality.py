from rectangles import loadRectangles
import os
from urllib.request import urlopen
    
def processAirQualityFiles(pollutant, years, rectangleFile, inputDirectory, printPrefixString = ""):
        
    data = {}
    
    rectangles = []
    loadRectangles(rectangles, rectangleFile, printPrefixString)

    stationRectanlgeId = {}
    stations = []
    for rectangle in rectangles:
        stationRectanlgeId[rectangle.name] = str(rectangle.ID)
        stations.append(rectangle.name)
        
    for station in stations:
        data[stationRectanlgeId[station]] = {}
    
    for year in years:
        for station in stations:
            
            fileName = inputDirectory + str(station) + "_" + str(year) + ".csv"
            
            print(printPrefixString + "Load data from " + fileName + "...")
            
            loadFile(pollutant, fileName, data[stationRectanlgeId[station]])
    
    return data
            
    
def loadFile(pollutant, fileName, data):

    if os.path.exists(fileName) == False:
        return

    firstLine = True
    firstRecord = True
    
    pollutantColumn = 0
    pollutantMultiplier = 1.0
    timeMinusOne = False
    
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:
            # skip the first line (header line)
            
            # remove newline character from the end
            line = line.rstrip()
             
            # split the line
            splittedLine = line.split(',')

            if firstLine == True:
                
                for i in range(2, len(splittedLine)):
                
                    if pollutant in splittedLine[i].lower():
                        pollutantColumn = i
                        if "ppb" in splittedLine[i].lower():
                            pollutantMultiplier = 1.913
                        break
                    
                firstLine = False
                continue
            
            # create date: 01/01/2013,01:00
            
            if len(splittedLine[0]) < 1:
                continue
            
            hour = int(splittedLine[1][0:2])
            
            if firstRecord:
                firstRecord = False
                if hour == 1:
                    timeMinusOne = True

            if timeMinusOne:
                if hour == 0:
                    hour = 23
                else:
                    hour = hour - 1
            
            if hour < 10:
                hourString = "0" + str(hour)
            else:
                hourString = str(hour)
            timestampString = splittedLine[0][6:10] + splittedLine[0][3:5] + splittedLine[0][0:2] + hourString
            
            if len(splittedLine[pollutantColumn]) < 1:
                continue
            
            try:
                data[timestampString] = float(splittedLine[pollutantColumn]) * pollutantMultiplier
            except:
                pass

def writeOutAnnualAverages(data, years, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "Writing out annual averages to " + outputFile + "...")
    
    avg = {}
    for station in data:
        avg[station] = {}
    
    for station in data:
        for year in years:
            mean = 0.0
            counter = 0
            for timestamp in data[station]:
                #print(timestamp[0:4])
                if timestamp[0:4] == str(year):
                    mean = mean + data[station][timestamp]
                    counter = counter + 1
            if counter > 0:
                mean = mean / float(counter)
            else:
                mean = None
            avg[station][year] = mean

    for station in data:
        for year in years:
            if avg[station][year] != None:
                print(printPrefixString + "\t" + str(station) + " in " + str(year) + ": " + str(avg[station][year]))
    
    output = open(outputFile, 'w')
    # header 
    output.write("location,year,annual\n")
    
    for station in data:
        for year in years:
            if avg[station][year] != None:
                output.write(str(station) + "," + str(year) + "," + str(avg[station][year]) + "\n")
    output.close()
    
    print(printPrefixString + "Done...")

def writeOutHourlyData(data, outputFile, printPrefixString = ""):
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,target\n")    
    
    for location in data:
        for timestamp in data[location]:
            output.write(str(location))
            output.write(",")
            output.write(str(timestamp))
            output.write(",")
            output.write(str(data[location][timestamp]))
            output.write("\n")
            
    output.close()
    
def downloadYorkAirqualityData(firstTimestamp, lastTimestamp, rectangleFile, printPrefixString = ""):

    # load rectangles
    rectangles = []
    loadRectangles(rectangles, rectangleFile, printPrefixString)
    
    startDate = firstTimestamp.key[0:4] + "-" + firstTimestamp.key[4:6] + "-" + firstTimestamp.key[6:8]
    endDate = lastTimestamp.key[0:4] + "-" + lastTimestamp.key[4:6] + "-" + lastTimestamp.key[6:8]
    
    urls = {}
    urls["Heworth"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK13&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Bootham"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK10&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Fulford"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK16&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Gillygate"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK7&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Holgate"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK8&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Lawrence"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK9&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    urls["Nunnery"] = "http://www.airqualityengland.co.uk/site/data.php?site_id=YK15&parameter_id%5B%5D=NO2&f_date_started=" + startDate + "&f_date_ended=" + endDate + "&la_id=76&action=download"
    
    aqData = {}
    
    for rectangle in rectangles:
        station = rectangle.name
        if station == "Fishergate":
            continue
        
        print(printPrefixString + "Downloading data for " + station + "...")
 
        url = urls[station]
        print(printPrefixString + "url: " + url)
        response = urlopen(url).read().decode("utf-8")
        r1 = response[response.find("<tr>") + 4:]
        r1 = r1[r1.find("<tr>") + 4:]
     
        while True:
             
            if r1.find("<tr>") == -1:
                break
             
            r1 = r1[r1.find("<tr>") + 4:]
            r1 = r1[r1.find("<td>") + 4:]
            dateString = r1[0:r1.find("</td>")]
            r1 = r1[r1.find("<td") + 3:]
            r1 = r1[r1.find(">") + 1:]
            timeString = r1[0:r1.find("</td>")]
            r1 = r1[r1.find("<td>") + 4:]
            levelString = r1[0:r1.find("</td>")]
            
            # 16/06/2016
            #24:00:00&nbsp;#
            hour = int(timeString[0:2]) - 1
            if hour < 10:
                timestampKey = dateString[6:10] + dateString[3:5] + dateString[0:2] + "0" + str(hour)
            else:
                timestampKey = dateString[6:10] + dateString[3:5] + dateString[0:2] + str(hour)
                
            if timestampKey not in aqData:
                aqData[timestampKey] = {}

            try:
                aqData[timestampKey][rectangle.ID] = float(levelString)
            except:
                continue
    return aqData
