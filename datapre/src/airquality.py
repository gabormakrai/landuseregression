from rectangles import loadRectangles

def processAirQualityFile(inputFile, inputRectangleFile, outputFile, printPrefixString = ""):
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Writing out air quality data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,nox\n")

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
            
            # create date: 01/01/2013,01:00
            hour = int(splittedLine[1][0:2])-1
            if hour < 10:
                hourString = "0" + str(hour)
            else:
                hourString = str(hour)
            timestampString = splittedLine[0][6:10] + splittedLine[0][3:5] + splittedLine[0][0:2] + hourString
    
            noxData = {}
    
            # bootham_nox
            if splittedLine[2] != "" and splittedLine[3] != "":
                nox = float(splittedLine[2]) + float(splittedLine[3])
                noxData["bootham"] = str(nox)
                
            #fulford_nox
            if splittedLine[10] != "" and splittedLine[11] != "":
                nox = float(splittedLine[10]) + float(splittedLine[11])
                noxData["fulford"] = str(nox)
            
            #gillygate_nox
            if splittedLine[12] != "" and splittedLine[13] != "":
                nox = float(splittedLine[12]) + float(splittedLine[13])
                noxData["gillygate"] = str(nox)
            
            #heworth_nox
            if splittedLine[14] != "" and splittedLine[15] != "":
                nox = float(splittedLine[14]) + float(splittedLine[15])
                noxData["heworth"] = str(nox)
            
            #holgate_nox
            if splittedLine[16] != "" and splittedLine[17] != "":
                nox = float(splittedLine[16]) + float(splittedLine[17])
                noxData["holgate"] = str(nox)
            
            #lawrence_nox
            if splittedLine[19] != "" and splittedLine[20] != "":
                nox = float(splittedLine[19]) + float(splittedLine[20])
                noxData["lawrence"] = str(nox)
    
            #nunnery_nox
            if splittedLine[21] != "" and splittedLine[22] != "":
                nox = float(splittedLine[21]) + float(splittedLine[22])
                noxData["nunnery"] = str(nox)
                
            #fishergate_nox
            if splittedLine[6] != "" and splittedLine[7] != "":
                nox = float(splittedLine[6]) + float(splittedLine[7])
                noxData["fishergate"] = str(nox)
            
            for stationName in noxData:
                # find out station id
                location = -1
                for rectangle in rectangles:
                    if rectangle.name.lower() == stationName:
                        location = rectangle.ID
                
                output.write(str(location))
                output.write(",")
                output.write(timestampString)
                output.write(",")
                output.write(noxData[stationName])
                output.write("\n")

    output.close()

    print(printPrefixString + "Done...")
    