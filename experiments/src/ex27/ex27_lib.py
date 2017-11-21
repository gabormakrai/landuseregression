
columnsGrouped = {
    "T": ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day'],
    "W": ['winddirection', 'windspeed', 'temperature', 'rain', 'pressure'],
    "A": ['atc'],
    "R": ['lane_length', 'length'],
    "L": ['landuse_area', 'leisure_area'],
    "B": ['buildings_area', 'buildings_number']
    }

def getTagAndFeatures(dataGroup):
    tag = ""
    for d in dataGroup:
        tag = tag + d
    features = []
    for dg in dataGroup:
        for d in columnsGrouped[dg]:
            features.append(d)
    return tag, features

def generateAllDataGroups():
    dataGroups = []
    for t in [True, False]:
        for w in [True, False]:
            for a in [True, False]:
                for r in [True, False]:
                    for l in [True, False]:
                        for b in [True, False]:
                            dataGroup = []
                            if t: dataGroup.append("T")
                            if w: dataGroup.append("W")
                            if a: dataGroup.append("A")
                            if r: dataGroup.append("R")
                            if l: dataGroup.append("L")
                            if b: dataGroup.append("B")
                            if len(dataGroup) == 0:
                                continue
                            dataGroups.append(dataGroup) 
    
    return dataGroups

def loadX(fileName, expected_features):
    X = []
    
    firstLine = True
    # open the file
    with open(fileName) as infile:
        # read line by line
        for line in infile:                
            # remove newline character from the end
            line = line.rstrip()
            
            splittedLine = line.split(",")
            
            # parse header
            if firstLine == True:
                firstLine = False
                if len(splittedLine) != len(expected_features):
                    print("trainX reading failed as wrong features have been loaded")
                    print("expected: " + str(expected_features))
                    print("actual: " + str(splittedLine))
                    exit()
                for i in range(0, len(expected_features)):
                    if expected_features[i] != splittedLine[i]:
                        print("trainX reading failed as wrong features have been loaded")
                        print("expected: " + str(expected_features))
                        print("actual: " + str(splittedLine))
                        exit()
                continue
            
            dataRow = []
            for i in range(0, len(splittedLine)):
                dataRow.append(float(splittedLine[i]))
            X.append(dataRow)
    return X

def loadSingleColumnsFile(fileName):
    data = []
    
    firstLine = True
    with open(fileName) as infile:
        for line in infile:                
            line = line.rstrip()
            if firstLine == True:
                firstLine = False
                continue
            data.append(float(line))
    return data
