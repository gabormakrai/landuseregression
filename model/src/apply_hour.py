import numpy as np
from norm import NONORMALIZATION
from models.model_decisiontree import trainDecisionTree, applyDecisionTree
from models.model_randomforest import trainRandomForest, applyRandomForest
from sklearn import tree

import time
from data.data import loadData

# open train data

dataFile1 = "/media/sf_lur/data/data_hour.csv"
data1 = {}
columns1 = []
loadData(dataFile1, ["location", "timestamp"], data1, columns1)

modelViz = trainDecisionTree(data1, columns1, "target", {'depth': 4})
print(str(modelViz.modelColumns))
tree.export_graphviz(modelViz.model, out_file='/media/sf_lur/data/dtr.dot', feature_names=modelViz.modelColumns, max_depth=8)     

exit()

start = time.time()
model = trainRandomForest(data1, columns1, "target", {'estimators': 59, 'leaf': 9})

# importances = model.model.feature_importances_
# std = np.std([tree.feature_importances_ for tree in model.model.estimators_],
#              axis=0)
# indices = np.argsort(importances)[::-1]
# print("Feature ranking:")
# for f in range(0,len(model.modelColumns)):
#     print(model.modelColumns[indices[f]] + " -> " + str(importances[indices[f]]))

end = time.time()
print(end - start)

# load apply data
dataFile2 = "/media/sf_lur/data/grid_hour.csv"
data2 = {}
columns2 = []
loadData(dataFile2, [], data2, columns2)
 
start = time.time()
         
predictionData = applyRandomForest(data2, model, {'estimators': 59, 'leaf': 9})
 
end = time.time()
print(end - start)
 
output = open("/media/sf_lur/data/apply_grid.csv", 'w')
output.write("location,timestamp,prediction\n")
for i in range(0, len(predictionData)):
    output.write(str(int(data2["location"][i])) + "," + str(int(data2["timestamp"][i])) + "," + str(predictionData[i]))
    output.write("\n")
 
output.close()
