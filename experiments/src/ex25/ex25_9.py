from ex25.ex25_lib import loadX, loadSingleColumnsFile
from eval.rmse import rmseEval
from sklearn.ensemble.forest import RandomForestClassifier

INPUT_DIRECTORY = "/experiments/ex25/"

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']
top16tags = ['TWL', 'TW', 'TWA', 'AL', 'WA', 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 
top16preds = ["pred_" + tag for tag in top16tags]

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

for location in locations:
    print("Location: " + str(location))
                
    trainX = loadX(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainX.csv", all_features)
    trainY = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainY.csv")
    trainPreds = []
    
    for tag in top16tags:
        p = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_trainPred_" + tag + ".csv")
        for i in range(0, len(p)):
            trainX[i].append(p[i])
        trainPreds.append(p)
    
    bestPossibleY = []

    labelY = []
    for i in range(0, len(trainY)):
        bestAbs = abs(trainY[i] - trainPreds[0][i])
        bestIndex = 0
        bestP = trainPreds[0][i]
        for j in range(0, len(top16tags)):
            modelAbs = abs(trainY[i] - trainPreds[j][i])
            if modelAbs < bestAbs:
                bestAbs = modelAbs
                bestIndex = j
                bestP = trainPreds[j][i]
        labelY.append(bestIndex)
        bestPossibleY.append(bestP)
    
    print("#trainX: " + str(len(trainX)) + ", #trainY: " + str(len(trainY)))
        
    rmse = rmseEval(trainPreds[1], trainY)[1]
    print("T+W Rmse: " + str(rmse))
    rmse = rmseEval(bestPossibleY, trainY)[1]
    print("Best Possible Rmse: " + str(rmse))
    
    model = RandomForestClassifier(random_state=42, n_estimators=60, max_depth=12)
    model.fit(trainX, labelY)
    
    trainPredY = model.predict(trainX)

    prediction = []
    for i in range(0, len(labelY)):
        p = trainPreds[trainPredY[i]][i]
        prediction.append(p)
        
    rmse = rmseEval(prediction, trainY)[1]
    print("Combined train Rmse: " + str(rmse))
    
    testX = loadX(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testX.csv", all_features)
    testY = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testY.csv")
    testPreds = []
    
    for tag in top16tags:
        p = loadSingleColumnsFile(INPUT_DIRECTORY + "z_" + str(int(location)) + "_testPred_" + tag + ".csv")
        for i in range(0, len(p)):
            testX[i].append(p[i])
        testPreds.append(p)
    
    testPredY = model.predict(testX)

    prediction = []
    for i in range(0, len(testPredY)):
        p = testPreds[testPredY[i]][i]
        prediction.append(p)
    
    rmse = rmseEval(testPreds[1], testY)[1]
    print("T+W test Rmse: " + str(rmse))
    rmse = rmseEval(prediction, testY)[1]
    print("Combined test Rmse: " + str(rmse))
