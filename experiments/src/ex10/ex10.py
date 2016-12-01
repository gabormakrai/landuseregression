from data.data import loadData
from crossvalidation import findOutKForValidation
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

def doEval(dayNight, landuse, topo, traffic_static, traffic_dynamic, weather, time, output):
    
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
    
    columnsToUse = []
    
    if landuse == True:
        columnsToUse.append('leisure_area')
        columnsToUse.append('landuse_area')
    if topo == True:
        columnsToUse.append('buildings_number')
        columnsToUse.append('buildings_area')
    if traffic_static == True:
        columnsToUse.append('lane_length')
        columnsToUse.append('length')
    if traffic_dynamic == True:
        columnsToUse.append('traffic_length_car')
        columnsToUse.append('traffic_length_lgv')
        columnsToUse.append('traffic_length_hgv')
    if weather == True:
        columnsToUse.append('winddirection')
        columnsToUse.append('windspeed')
        columnsToUse.append('temperature')
        columnsToUse.append('rain')
        columnsToUse.append('pressure')
    if time == True:
        columnsToUse.append('hour')
        columnsToUse.append('day_of_week')
        columnsToUse.append('month')
        columnsToUse.append('bank_holiday')
        columnsToUse.append('race_day')

    data = {}
    columns = []
    loadData(dataFile, ['timestamp'], data, columns)
    
    locationValues = findOutKForValidation("location", data)
    
    for location in locationValues:
        
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, columnsToUse, "target", dayNight)
        
        print("\t" + str(len(trainX)) + "," + str(len(testX)))
        
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = 1, random_state=42)
        
        model.fit(trainX, trainY)
        
        prediction = model.predict(testX)
        
        rmse = rmseEval(testY, prediction)
        
        print("\t" + str(rmse))
        
        output.write(str(dayNight) + ",")
        output.write(groupName + ",")
        output.write(str(rmse[1]) + "\n")
        output.flush()

outputFile = "/media/sf_lur/experiments/ex10/result_rfr.csv"

dataFile = "/media/sf_lur/data/data_hour_2013.csv"

output = open(outputFile, 'w')

output.write("day_night,group,RMSE\n")

# doEval(True, False, False, False, False, True, True, output)
# doEval(False, False, False, False, False, True, True, output)

for landuse in [True, False]:
    for topo in [True, False]:
        for traffic_static in [True, False]:
            for traffic_dynamic in [True, False]:
                for weather in [True, False]:
                    for time in [True, False]:
                        doEval(True, landuse, topo, traffic_static, traffic_dynamic, weather, time, output)
                        doEval(False, landuse, topo, traffic_static, traffic_dynamic, weather, time, output)

output.close()
