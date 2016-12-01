from eval.rmse import rmseEval
from data.data import loadData
from norm import NONORMALIZATION
from crossvalidation import crossValidation
import random
from models.model_nearestneighbors import trainNearestNeighbors,\
    applyNearestNeighbors

# parameters

k = 8

parametersList = []
for d in ["distance", "uniform"]:
    for p in range(1, 4):
        for n in range(3, 10):
            parametersList.append({"p": p, "neighbors": n, "weights": d})

evalFunctions = [rmseEval]

# load the data
data1 = {}
columns1 = []
loadData("/media/sf_lur/data/data_hour_2013.csv", ["location", "timestamp"], data1, columns1)

for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data1, columns1, "target", NONORMALIZATION, trainNearestNeighbors, applyNearestNeighbors, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
    
# load the data
data2 = {}
columns2 = []
loadData("/media/sf_lur/data/data_hour_2013.csv", ["location", "timestamp"], data2, columns2)
 
for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data2, columns2, "target", NONORMALIZATION, trainNearestNeighbors, applyNearestNeighbors, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))