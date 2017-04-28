from data.data import loadData
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from crossvalidation import splitDataForXValidation1

outputFile = "/media/sf_lur/experiments/ex20/fig3.csv"
DATA_FILE = "/media/sf_lur/data/data3_hour_2013.csv"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

output = open(outputFile, 'w')
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
            
    columnsToSkip = ['timestamp']
    
    if landuse == False:
        columnsToSkip.append('leisure_area')
        columnsToSkip.append('landuse_area')
    if topo == False:
        columnsToSkip.append('buildings_number')
        columnsToSkip.append('buildings_area')
    if traffic_static == False:
        columnsToSkip.append('lane_length')
        columnsToSkip.append('length')
    if traffic_dynamic == False:
        columnsToSkip.append('atc')
    if weather == False:
        columnsToSkip.append('winddirection')
        columnsToSkip.append('windspeed')
        columnsToSkip.append('temperature')
        columnsToSkip.append('rain')
        columnsToSkip.append('pressure')
    if time == False:
        columnsToSkip.append('hour')
        columnsToSkip.append('day_of_week')
        columnsToSkip.append('month')
        columnsToSkip.append('bank_holiday')
        columnsToSkip.append('race_day')

    columns = []
    data = {}
    loadData(DATA_FILE, columnsToSkip, data, columns)
        
    # modelling
    for location in locations:
        
        print("Location: " + str(location))
          
        trainX, testX, trainY, testY = splitDataForXValidation1(location, "location", data, columns, "target")
        print("\tRFR #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        rmse = rmseEval(testY, prediction)[1]
        print("\trmse: " + str(rmse))
        output.write(str(groupName) + "," + str(rmse) + "\n")        

for landuse in [True, False]:
    for topo in [True, False]:
        for traffic_static in [True, False]:
            for traffic_dynamic in [True, False]:
                for weather in [True, False]:
                    for time in [True, False]:
                        doEval(landuse, topo, traffic_static, traffic_dynamic, weather, time, output)

#doEval(True, False, True, False, False, True, output)

output.close()
