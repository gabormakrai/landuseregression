from data.data import loadData
from ex27.crossvalidation import splitDataForXValidationSampled
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval
from ex27.ex27_lib import generateAllDataGroups, getTagAndFeatures

DATA_FILE = "/data/york3_hour_2013.csv"
OUTPUT_DIRECTORY = "/experiments/ex27/"

locations = [2.0, 3.0, 4.0, 6.0, 8.0]

data = {}
columns = []
loadData(DATA_FILE, ['timestamp'], data, columns)

sampleRate = 0.75

top16tags = ['TW','TWA','W','TWL','TWB','T','WA','WB','TA','TWRLB','A','TWAB','TWRL','WL','TWARLB','TWAL']

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

top16datagroups = []
data_groups = generateAllDataGroups()
for tag in top16tags:
    for datagroup in data_groups:
        dgtag, _ = getTagAndFeatures(datagroup)
        if dgtag == tag:
            top16datagroups.append(datagroup)
            break

all_tags, all_features = getTagAndFeatures(['T','W', 'A', 'R', 'L', 'B'])
 
for location in locations:
    print("Location: " + str(location))
    trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled(location, "location", sampleRate, 42, data, all_features, "target")
    
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainX.csv", all_features, trainX2)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testX.csv", all_features, testX)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainY.csv", ["target"], trainY2)
    writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testY.csv", ["target"], testY)
    
    for dataGroup in generateAllDataGroups():
        tag, features = getTagAndFeatures(dataGroup)
        trainX1, trainX2, trainY1, trainY2, testX, testY = splitDataForXValidationSampled(location, "location", sampleRate, 42, data, features, "target")
        model = RandomForestRegressor(min_samples_leaf = 9, n_estimators = 59, n_jobs = -1, random_state=42)                    
        model.fit(trainX1, trainY1)
        trainPrediction = model.predict(trainX2)
        testPrediction = model.predict(testX)
        trainRmse = str(rmseEval(trainY2, trainPrediction)[1])
        testRmse = str(rmseEval(testY, testPrediction)[1])
        print("\t" + tag + ": #train: " + str(len(trainY2)) + ", #test:" + str(len(testY)) + ", trainRMSE: " + trainRmse + ", testRMSE: " + testRmse)
        writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_trainPred_" + tag + ".csv", ["trainPred_" + tag], trainPrediction)
        writeOutData(OUTPUT_DIRECTORY + "z_" + str(int(location)) + "_testPred_" + tag + ".csv", ["testPred_" + tag], testPrediction)
        