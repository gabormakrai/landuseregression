from rectangles import loadRectangles
import os
    
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
    