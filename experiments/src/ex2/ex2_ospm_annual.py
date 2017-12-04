from data.data import loadData
from collections import defaultdict
from eval.rmse import rmseEval
from eval.mae import maeEval

INPUT_DIRECTORY = "/data/york_ospm/"
INPUT_DATA_FILE = "/data/york_hour_2013.csv"

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

observationPerStation = []
predictionPerStation = []
    
for station in stations:
    ospm = ospmData[station]
    obs = obsData[station]
    
    obs_avg = 0.0
    pred_avg = 0.0
    c = 0
    
    observations = []
    predictions = []
        
    for timestamp in ospm:
        if timestamp not in obs:
            continue
        pred = ospm[timestamp]
        o = obs[timestamp]
        
        observations.append(o)
        predictions.append(pred)
        
        c = c + 1
        obs_avg = obs_avg + o
        pred_avg = pred_avg + pred
    
    pred_avg = pred_avg / float(c)
    obs_avg = obs_avg / float(c)
    print("location: " + str(station))
    print("\tcounter: " + str(c))
    print("\tpred_avg: " + str(pred_avg))
    print("\tobs_avg: " + str(obs_avg))
    observationPerStation.append(obs_avg)
    predictionPerStation.append(pred_avg)
    rmse = rmseEval(observations, predictions)[1]
    print("\tRMSE: " + str(rmse))

rmse = rmseEval(observationPerStation, predictionPerStation)[1]
print("RMSE: " + str(rmse))
mae = maeEval(observationPerStation, predictionPerStation)[1]
print("MAE: " + str(mae))

