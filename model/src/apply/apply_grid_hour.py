from models.model_randomforest import trainRandomForest, applyRandomForest
from data.data import loadData
import os

DATA_DIRECTORY = "/media/sf_lur/data/"
OUTPUT_DIRECTORY = "/media/sf_lur/grid_hour/data/"

# open train data

dataFile1 = DATA_DIRECTORY + "data_hour_2013.csv"
data1 = {}
columns1 = []
loadData(dataFile1, ["location", "timestamp"], data1, columns1)
  
model = trainRandomForest(data1, columns1, "target", {'estimators': 59, 'leaf': 9})

fileNames = next(os.walk(DATA_DIRECTORY + "pre_grid_hour/data/"))[2]
for fileName in fileNames:
    inputFile = DATA_DIRECTORY + "pre_grid_hour/data/" + fileName
    outputFileName = OUTPUT_DIRECTORY + fileName 
     
    # load apply data
    dataFile2 = inputFile
    data2 = {}
    columns2 = []
    loadData(dataFile2, [], data2, columns2)
       
    predictionData = applyRandomForest(data2, model, {'estimators': 59, 'leaf': 9})
        
    output = open(outputFileName, 'w')
    output.write("location,timestamp,prediction\n")
    for i in range(0, len(predictionData)):
        output.write(str(int(data2["location"][i])) + "," + str(int(data2["timestamp"][i])) + "," + str(predictionData[i]))
        output.write("\n")
       
    output.close()
