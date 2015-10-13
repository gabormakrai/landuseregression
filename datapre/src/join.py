
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
                        if c != "location" and c != "timestampe":
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

