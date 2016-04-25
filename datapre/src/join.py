
def joinFiles(inputFiles, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "Joining data in preprocessed files (join on location+timestamp, target: nox)...")
    
    data = {}
    columns = set()
    
    for file in inputFiles:
        
        headersDictionary = {}
        headersArray = []
        
        fileColumns = set()
        
        print(printPrefixString + "\tOpen file " + file + "...")
        
        firstLine = True
        # open the file
        with open(file) as infile:
            # read line by line
            for line in infile:                
                # remove newline character from the end
                line = line.rstrip()
                
                # parse header
                if firstLine == True:
                    firstLine = False
                    parseHeader(line, headersDictionary, headersArray)
                    for c in headersDictionary:
                        if c != "location" and c != "timestamp":
                            fileColumns.add(c)
                            columns.add(c) 
                    continue
                
                # split the line
                splittedLine = line.split(',')
        
                location = splittedLine[headersDictionary["location"]]
                if location not in data:
                    data[location] = {}
                timestamp = splittedLine[headersDictionary["timestamp"]]
                if timestamp not in data[location]:
                    data[location][timestamp] = {}
                for c in fileColumns:
                    dataEntry = splittedLine[headersDictionary[c]]
                    data[location][timestamp][c] = dataEntry
                        
    print(printPrefixString + "Writing out data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    # header 
    output.write("location,timestamp,nox")
    for column in columns:
        if column != "location" and column != "timestamp" and column != "nox":
            output.write(",")
            output.write(column)
    output.write("\n")

    for location in data:
        for timestamp in data[location]:
            validRecord = True
            for c in columns:
                if c != "location" and c != "timestamp":
                    if c not in data[location][timestamp]:
                        validRecord = False
            if validRecord == False:
                continue
            output.write(location)
            output.write(",")
            output.write(timestamp)
            output.write(",")
            output.write(data[location][timestamp]["nox"])
            for column in columns:
                if column != "location" and column != "timestamp" and column != "nox":
                    output.write(",")
                    #print(location + "," + timestamp)
                    output.write(data[location][timestamp][column])
            output.write("\n")
            
    output.close()
        
    print(printPrefixString + "Done...")
    
def parseHeader(header, headersDictionary, headersArray):

    splittedHeader = header.split(",")
    for i in range(0,len(splittedHeader)):
        headersDictionary[splittedHeader[i]] = i
        headersArray.append(splittedHeader[i])

def loadDataFile(file, year, rangeString, data, printPrefixString = ""):
    
    print(printPrefixString + "Open " + file + " for data...")
    
    fileHeader = []
    
    firstLine = True
    # open the file
    with open(file) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            # split the line
            splittedLine = line.split(',')
            
            # parse header
            if firstLine == True:
                firstLine = False
                for c in splittedLine:
                    if c != "location":
                        fileHeader.append(c + "_" + rangeString)
#                 print(str(fileHeader))
                continue
            
            location = splittedLine[0]
            
            for i in range(1, len(splittedLine)):
                
                if location not in data:
                    data[location] = {}
                if year not in data[location]:
                    data[location][year] = {}
                
                data[location][year][fileHeader[i - 1]] = splittedLine[i]
            
def joinYear(fileTypes, years, ranges, inputDirectory, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "Joining the data in " + inputDirectory + " folder...")
    
    # data[location][year][column]...
    data = {}
    
    for file in fileTypes:
        for year in years:
            for r in ranges:
                y = str(year)
                fileName = inputDirectory + file + "_" + r + "_" + y + ".csv"
                loadDataFile(fileName, y, r, data, printPrefixString + "\t")


    openAirQualityFileAndWriteOutData(inputDirectory + "aq.csv", data, outputFile, printPrefixString)
                    
    print(printPrefixString + "Done")
     
def openAirQualityFileAndWriteOutData(aqFile, data, outputFile, printPrefixString):
    print(printPrefixString + "Open " + aqFile + " for data...")
    print(printPrefixString + "And writing out " + outputFile + " data file...")
    
    dataColumns = []
    
    output = open(outputFile, 'w')
    
    firstLine = True
    # open the file
    with open(aqFile) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            # split the line
            splittedLine = line.split(',')
            
            # parse header
            if firstLine == True:
                firstLine = False
                continue
            
            location = splittedLine[0]
            year = splittedLine[1]
            target = splittedLine[2]
            
            if len(dataColumns) == 0:
                for c in data[location][year]:
                    dataColumns.append(c)
                dataColumns.sort()
                print(str(dataColumns))
                output.write("location,year")
                for c in dataColumns:
                    output.write("," + c)
                output.write(",target\n")
            
            output.write(location + ",")
            output.write(year)
            for c in dataColumns:
                output.write("," + data[location][year][c])
            output.write("," + target + "\n")
    output.close()
    
def joinYearForApply(fileTypes, year, ranges, inputDirectory, outputFile, printPrefixString = ""):
    
    print(printPrefixString + "Joining the data in " + inputDirectory + " folder...")
    
    # data[location][year][column]...
    data = {}
    
    for file in fileTypes:
        for r in ranges:
            y = str(year)
            fileName = inputDirectory + file + "_" + r + "_" + y + ".csv"
            loadDataFile(fileName, y, r, data, printPrefixString + "\t")

    openAirQualityFileAndWriteOutDataApply(data, str(year), outputFile, printPrefixString)
                    
    print(printPrefixString + "Done")

def openAirQualityFileAndWriteOutDataApply(data, year, outputFile, printPrefixString):
    print(printPrefixString + "And writing out " + outputFile + " data file...")
    
    dataColumns = []
    
    output = open(outputFile, 'w')
    
    for location in data:
        if len(dataColumns) == 0:
            for c in data[location][year]:
                dataColumns.append(c)
            dataColumns.sort()
            print(str(dataColumns))
            output.write("location,year")
            for c in dataColumns:
                output.write("," + c)
            output.write("\n")
    
        output.write(location + ",")
        output.write(year)
        for c in dataColumns:
            output.write("," + data[location][year][c])
        output.write("\n")
    output.close()
