from data.data import loadData
from collections import defaultdict

INPUT_DIRECTORY = "/data/york_ospm/"
INPUT_DATA_FILE = "/data/york_hour_2013.csv"
OUTPUT_DATA_FILE = "/experiments/ex2/ex2_ospm.csv"

stations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
stationNames = {2.0: "Fulford", 3.0: "Gillygate", 4.0: "Heworth", 5.0: "Holgate", 6.0: "Lawrence", 7.0: "Nunnery", 8.0: "Fishergate"}

def loadOspmData(fileName, d, location):
    
    print("Opening ospm output file " + fileName + "...")
    firstLine = True
    
    d[location] = {}
    
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
            
            d[location][timestampString] = cLevel
    print("done...")

# load the data
data = {}
columns = []
loadData(INPUT_DATA_FILE, [], data, columns)

obsData = defaultdict(lambda: defaultdict(lambda: 0.0))

for i in range(0, len(data["target"])):
    l = data["location"][i]
    t = str(int(float(data["timestamp"][i])))
    o = data["target"][i]
    obsData[l][t] = o

ospmData = {}

for location in stations:
    loadOspmData(INPUT_DIRECTORY + stationNames[location].lower() + "_2013.dat", ospmData, location)
    
output = open(OUTPUT_DATA_FILE, 'w')
output.write("location,observation,prediction\n")

for station in stations:
    ospm = ospmData[station]
    obs = obsData[station]
    
    for timestamp in ospm:
        if timestamp not in obs:
            continue
        pred = ospm[timestamp]
        o = obs[timestamp]
        
        output.write(str(station))
        output.write(",")
        output.write(str(o))
        output.write(",")
        output.write(str(pred))
        output.write("\n")

output.close()
