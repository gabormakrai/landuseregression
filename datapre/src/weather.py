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