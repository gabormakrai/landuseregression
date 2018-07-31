from ex29.crossvalidation import splitDataForXValidation
from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

OUTPUT_DATA_FILE = "/experiments/ex29/ex29_8.csv"
DATA_FILE = "/data/london3_hour_2016.csv"

groups = [['71.0', '70.0', '38.0', '55.0', '91.0', '73.0', '89.0'],
['5.0', '29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0', '13.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0', '51.0']]

# load the data
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

output = open(OUTPUT_DATA_FILE, 'w')
output.write("group,rmse\n")

def doEval(landuse, topo, traffic_static, traffic_dynamic, weather, time, output):
    
    if landuse == False and topo == False and traffic_dynamic == False and traffic_static == False and weather == False and time == False:
        return
    
    groupName = "lu"
    if landuse == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "to"
    if topo == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
    
    groupName = groupName + "ts"
    if traffic_static == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "td"
    if traffic_dynamic == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "we"
    if weather == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    groupName = groupName + "ti"
    if time == True:
        groupName = groupName + "1"
    else:
        groupName = groupName + "0"
        
    print("Group: " + groupName)
        
    features = []
    
    if landuse:
        features.extend(['natural_area', 'leisure_area', 'landuse_area'])
    if topo:
        features.extend(['building_area', 'building_count'])
    if traffic_static:
        features.extend(['lane_length', 'length'])
    if traffic_dynamic:
        features.append('atc')
    if weather:
        features.append('winddirection')
        features.append('winddirection')
        features.append('temperature')
        features.append('rain')
        features.append('humidity')
        features.append('pressure')
    if time:
        features.append('hour')
        features.append('day_of_week')
        features.append('month')
        features.append('bank_holiday')
        
    all_observations = []
    all_predictions = []

    for group in range(0, len(groups)):
        trainStations = []
        for i in range(0, len(groups)):
            if i != group:
                trainStations.extend(groups[i]) 
        testStations = groups[group]
        
        train_station_set = set([float(s) for s in trainStations])
        test_station_set = set([float(s) for s in testStations])
        
        trainX, testX, trainY, testY = splitDataForXValidation(train_station_set, test_station_set, "location", data, features, "target")
        model = RandomForestRegressor(min_samples_leaf = 29, n_estimators = 64, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        all_observations.extend(testY)
        all_predictions.extend(prediction)
            
    rmse = rmseEval(all_observations, all_predictions)[1]
    output.write(str(groupName) + "," + str(rmse) + "\n")
    output.flush()

for landuse in [True, False]:
    for topo in [True, False]:
        for traffic_static in [True, False]:
            for traffic_dynamic in [True, False]:
                for weather in [True, False]:
                    for time in [True, False]:
                        doEval(landuse, topo, traffic_static, traffic_dynamic, weather, time, output)

output.close()
