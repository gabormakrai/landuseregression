
def loadOSPMData(fileName, data, stationName, printPrefixString = ""):
    
    print(printPrefixString + "Opening ospm output file " + fileName + "...")
    firstLine = True
    
    data[stationName] = {}
    
    with open(fileName) as infile:
        # read line by line
        for line in infile:
            
            if firstLine == True:
                firstLine = False
                continue
                            
            # remove newline character from the end
            line = line.rstrip()
                    
            # split the line
            splittedLine = line.split(' ')
            
            cLevel = None
            hour = None
            year = None
            day = None
            month = None
            
            for s in splittedLine:
                if s != "":
                    if cLevel == None:
                        cLevel = float(s)
                    elif year == None:
                        year = s
                    elif month == None:
                        month = int(s)
                    elif day == None:
                        day = int(s)
                    else:
                        hour = int(s) - 1
             
            if hour < 10:
                hourString = "0" + str(hour)
            else:
                hourString = str(hour)
            if day < 10:
                dayString = "0" + str(day)
            else:
                dayString = str(day)
            if month < 10:
                monthString = "0" + str(month)
            else:
                monthString = str(month)
                
            timestampString = year + monthString + dayString + hourString
            
            #print(timestampString + " -> " +str(cLevel))
            data[stationName][timestampString] = cLevel
    print(printPrefixString + "done...")
    