from data.data import loadData
from ex25.crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from builtins import isinstance
from ex25.ex25_lib import getTagAndFeatures, generateAllDataGroups

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_DIRECTORY = "/experiments/ex25/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

timestampDoubleData = data["timestamp"]
timestampData = []
for v in timestampDoubleData:
    timestampData.append(str(int(v)))

def writeOutData(fileName, columns, data):
    output = open(fileName, 'w')
    firstColumn = True
    for c in columns:
        if firstColumn:
            firstColumn = False
        else:
            output.write(",")
        output.write(c)
    output.write("\n")
    
    for i in range(0, len(data)):
        if isinstance(data[i], list):
            for j in range(0, len(data[i])):
                if j != 0:
                    output.write(",")
                output.write(str(data[i][j]))
        else:
            output.write(str(data[i]))
        output.write("\n")
    output.close()
    
all_tags, all_features = getTagAndFeatures(['T','W', 'A', 'R', 'L', 'B'])

print(str(all_features))
    
for location in locations:
    print("location: " + str(location))
    # save down trainX, trainY, testX, testY
    trainX, testX, trainY, testY, _, _ = splitDataForXValidation(location, "location", data, all_features, "target", timestampData)
    print("\t#train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
    
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainX.csv", all_features, trainX)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testX.csv", all_features, testX)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainY.csv", ["target"], trainY)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testY.csv", ["target"], testY)
    
    for dataGroup in generateAllDataGroups():
        tag, features = getTagAndFeatures(dataGroup)
        trainX, testX, trainY, testY, _, _ = splitDataForXValidation(location, "location", data, features, "target", timestampData)
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
        model.fit(trainX, trainY)
        trainPrediction = model.predict(trainX)
        testPrediction = model.predict(testX)
        trainRmse = str(rmseEval(trainY, trainPrediction)[1])
        testRmse = str(rmseEval(testY, testPrediction)[1])
        print("\t" + tag + ": #train: " + str(len(trainY)) + ", #test:" + str(len(testY)) + ", trainRMSE: " + trainRmse + ", testRMSE: " + testRmse)
        writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainPred_" + tag + ".csv", ["trainPred_" + tag], trainPrediction)
        writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testPred_" + tag + ".csv", ["testPred_" + tag], testPrediction)
        
            