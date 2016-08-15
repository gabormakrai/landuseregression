from eval.rmse import rmseEval
from data.data import loadData
from norm import NONORMALIZATION
from crossvalidation import crossValidation
import random
from models.model_svm import trainSVM, applySVM

# parameters

k = 8

parametersList = []
for c in [100, 300, 600, 1000, 1200, 1500, 2000, 3000]:
    for estimators in range(5,21):
        for samples in [1000, 2000, 3000, 4000, 5000]:
            parametersList.append({"C": c, "max_samples": samples, "n_estimators": estimators})

evalFunctions = [rmseEval]
    
# load the data
data2 = {}
columns2 = []
loadData("/media/sf_lur/data/data_hour_2013.csv", ["location", "timestamp"], data2, columns2)
 
for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data2, columns2, "target", NONORMALIZATION, trainSVM, applySVM, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
