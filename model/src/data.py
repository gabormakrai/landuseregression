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
