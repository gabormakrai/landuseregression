from sklearn.ensemble.forest import RandomForestRegressor
from ex3.crossvalidation import splitDataForXValidation
from data.data import loadData
from eval.rmse import rmseEval

OUTPUT_DATA_FILE = "/experiments/ex3/ex3_1.csv"

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

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
        features.append('leisure_area')
        features.append('landuse_area')
    if topo:
        features.append('buildings_number')
        features.append('buildings_area')
    if traffic_static:
        features.append('lane_length')
        features.append('length')
    if traffic_dynamic:
        features.append('traffic_length_car')
        features.append('traffic_length_lgv')
        features.append('traffic_length_hgv')
    if weather:
        features.append('winddirection')
        features.append('windspeed')
        features.append('temperature')
        features.append('rain')
        features.append('pressure')
    if time:
        features.append('hour')
        features.append('day_of_week')
        features.append('month')
        features.append('bank_holiday')
        features.append('race_day')
    
    all_obs = []    
    all_prediction = []
    
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, features, "target")
        model = RandomForestRegressor(min_samples_leaf = 2, random_state=42, n_estimators=650, n_jobs=-1)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        all_obs.extend(testY)
        all_prediction.extend(prediction)
        
    rmse = rmseEval(all_obs, all_prediction)[1]
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
