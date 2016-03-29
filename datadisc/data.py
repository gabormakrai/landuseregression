
def loadFile(file, data, printPrefixString = ""):
    
    headersArray = []
    
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
                splittedHeader = line.split(",")
                for h in splittedHeader:
                    data[h] = []
                    headersArray.append(h)                    
                continue
            
            # split the line
            splittedLine = line.split(',')
            
            for i in range(0, len(splittedLine)):
                data[headersArray[i]].append(splittedLine[i])
    

def parseHeader(header, headersDictionary, headersArray):

    for i in range(0,len(splittedHeader)):
        headersDictionary[splittedHeader[i]] = i
        headersArray.append(splittedHeader[i])                