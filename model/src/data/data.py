"""
File contains data for loading the data from the data preprocessing phase
"""

def loadData(fileName, columnToSkip, data, columnsToReturn):
    
    print("Loading " + fileName + " data file...")
    
    firstLine = True
    
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:
            # remove newline character from the end
            line = line.rstrip()
            # split the line
            splittedLine = line.split(',')
            # first line (header line)
            if firstLine == True:
                firstLine = False
                columns = splittedLine
                for column in columns:
                    if column not in columnToSkip:
                        data[column] = []
                continue
            
            for i in range(0, len(columns)):
                if columns[i] in columnToSkip:
                    continue
                data[columns[i]].append(float(splittedLine[i]))
            
    for column in columns:
        if column not in columnToSkip:
            columnsToReturn.append(column)

def loadEvalData(fileName, data):
    
    print("Loading " + fileName + " data file...")
    
    firstLine = True
    
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:
            # remove newline character from the end
            line = line.rstrip()
            # split the line
            splittedLine = line.split(',')
            # first line (header line)
            if firstLine == True:
                firstLine = False
                continue
            if splittedLine[0] not in data:
                data[splittedLine[0]] = {}
            if splittedLine[1] not in data[splittedLine[0]]:
                data[splittedLine[0]][splittedLine[1]] = []
                
            if splittedLine[2][0] == '[':
                data[splittedLine[0]][splittedLine[1]].append(float(splittedLine[2][1:len(splittedLine[2])-1]))
            else:
                data[splittedLine[0]][splittedLine[1]].append(float(splittedLine[2]))
    
    print("done...")
