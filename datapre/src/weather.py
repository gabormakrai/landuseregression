from rectangles import loadRectangles

def processWeatherFile(inputFile, inputRectangleFile, outputFile, printPrefixString):
    
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Writing out weather data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,winddirection,windspeed,temperature,humidity,pressure\n")

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
            
            for rectangle in rectangles:
                output.write(str(rectangle.ID))
                output.write(",")
                output.write(splittedLine[0])
                output.write(",")
                output.write(splittedLine[1])
                output.write(",")
                output.write(splittedLine[2])
                output.write(",")
                output.write(splittedLine[3])
                output.write(",")
                output.write(splittedLine[4])
                output.write(",")
                output.write(splittedLine[5])
                output.write("\n")

    output.close()

    print(printPrefixString + "Done...")
    
def processWeatherFileBinned(inputFile, inputRectangleFile, outputFile, printPrefixString):
    # load rectangles
    rectangles = []
    # load rectangle data
    loadRectangles(rectangles, inputRectangleFile, printPrefixString)
    
    print(printPrefixString + "Writing out weather data to " + outputFile + "...")
    
    output = open(outputFile, 'w')
    output.write("location,timestamp,")
    for i in range(0, 12):
        output.write("winddirection" + str(i) + ",")
    for i in range(0, 8):
        output.write("windspeed" + str(i) + ",")
    for i in range(0, 6):
        output.write("temperature" + str(i) + ",")
    for i in range(0, 10):
        output.write("humidity" + str(i) + ",")
    for i in range(0, 8):
        output.write("pressure" + str(i))
        if i == 7:
            output.write("\n")
        else:
            output.write(",")

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
            
            for rectangle in rectangles:
                output.write(str(rectangle.ID))
                output.write(",")
                output.write(splittedLine[0])
                output.write(",")
                # winddirection (30 degrees -> 12 variables)
                category = int(float(splittedLine[1]) / 30.0)
                for i in range(0, 12):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # windspeed (5 m/s bins -> 8 variables)
                category = int(float(splittedLine[2]) / 5.0)
                for i in range(0, 8):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # temperature (6 celsius degrees -> 6 variables)
                category = int(float(splittedLine[3]) / 5.0)
                for i in range(0, 6):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # humidity
                category = int(float(splittedLine[4]) / 10.0)
                for i in range(0, 10):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    output.write(",")
                # pressure
                category = int((float(splittedLine[5]) - 955.0) / 10.0)
                for i in range(0, 8):
                    if i == category:
                        output.write("1")
                    else:
                        output.write("0")
                    if i == 7:
                        output.write("\n")
                    else:
                        output.write(",")

    output.close()

    print(printPrefixString + "Done...")
