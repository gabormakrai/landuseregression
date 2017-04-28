from data.data import loadData
from norm import NONORMALIZATION
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from models.model_randomforest import trainRandomForest, applyRandomForest

import time

# open train data

dataFile1 = "/media/sf_Google_Drive/transfer/data/data_year.csv"
data1 = {}
columns1 = []
loadData(dataFile1, ["location", "year"], data1, columns1)

# train 
#models = []
#models.append({"name": "dtr", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": data1, "columns": columns1, "parameters": })
#models.append({"name": "rfr", "norm": NONORMALIZATION, "train": trainRandomForest, "apply": applyRandomForest, "data": data1, "columns": columns1, "parameters": })

start = time.time()

model = trainRandomForest(data1, columns1, "target", {'estimators': 59, 'leaf': 9})

end = time.time()
print(end - start)

# load apply data
dataFile2 = "/media/sf_Google_Drive/transfer/data/data_grid.csv"
data2 = {}
columns2 = []
loadData(dataFile2, ["year"], data2, columns2)

start = time.time()
        
predictionData = applyRandomForest(data2, model, {'estimators': 59, 'leaf': 9})

end = time.time()
print(end - start)

output = open("/media/sf_Google_Drive/transfer/data/apply_grid.csv", 'w')
output.write("location,prediction\n")
for i in range(0, len(predictionData)):
    output.write(str(int(data2["location"][i])) + "," + str(predictionData[i]))
    output.write("\n")

output.close()
