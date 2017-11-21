from ex25.ex25_lib import loadX, loadSingleColumnsFile
from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestClassifier

INPUT_DIRECTORY = "/experiments/ex25/"

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']
top16tags = ['TWL', 'TW', 'TWA', 'AL', 'WA', 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 
top16preds = ["pred_" + tag for tag in top16tags]

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

all_columns = all_features + top16preds

def evalColumns(columns, max_depth, n_estimators):

    overallY = []
    overallPred = []

    for location in locations:
                    
        trainX = loadX(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainX.csv", all_features)
        trainY = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainY.csv")
        trainPreds = []
        for tag in top16tags:
            p = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainPred_" + tag + ".csv")
            for i in range(0, len(p)):
                trainX[i].append(p[i])
            trainPreds.append(p)
        labelY = []
        for i in range(0, len(trainY)):
            bestAbs = abs(trainY[i] - trainPreds[0][i])
            bestIndex = 0
            for j in range(0, len(top16tags)):
                modelAbs = abs(trainY[i] - trainPreds[j][i])
                if modelAbs < bestAbs:
                    bestAbs = modelAbs
                    bestIndex = j
            labelY.append(bestIndex)
        
        # reduce trainX
        
        reducedTrainX = []
        for d in trainX:
            reducedD = []
            for i in range(0, len(all_columns)):
                if columns[i]:
                    reducedD.append(d[i])
            reducedTrainX.append(reducedD)
        
        model = RandomForestClassifier(random_state=42, n_estimators=n_estimators, max_depth=max_depth)
        model.fit(reducedTrainX, labelY)
                
        testX = loadX(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testX.csv", all_features)
        testY = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testY.csv")
        testPreds = []
        
        for tag in top16tags:
            p = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testPred_" + tag + ".csv")
            for i in range(0, len(p)):
                testX[i].append(p[i])
            testPreds.append(p)
            
        reducedTestX = []
        for d in testX:
            reducedD = []
            for i in range(0, len(all_columns)):
                if columns[i]:
                    reducedD.append(d[i])
            reducedTestX.append(reducedD)
            
        
        testPredY = model.predict(reducedTestX)
    
        prediction = []
        for i in range(0, len(testPredY)):
            p = testPreds[testPredY[i]][i]
            prediction.append(p)        
                
        overallY = overallY + testY
        overallPred = overallPred + prediction
    
    rmse = rmseEval(overallPred, overallY)[1]
    return rmse

columns = [True, False, False, False, True, False, True, True, True, True, False, True, False, False, False, False, False, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False]

for d in [12, 15, 18, 21]:
    for e in [60, 70, 80, 90, 100, 110, 120]:
        rmse = evalColumns(columns, d, e)
        print("max_depth: " + str(d) + ",n_est:" + str(e) + " -> " + str(rmse))
