from data import loadData
import random
from norm import NONORMALIZATION
from models.model_linearregression import trainLinearRegression,\
    applyLinearRegression
from eval.rmse import rmseEval
from eval.correlation import correlationEval
from eval.rsquared import rsquaredEval
from eval.mae import maeEval
from eval.nmse import nmseEval
from eval.fb import fbEval
from crossvalidation import crossValidation
from models.model_decisiontree import trainDecisionTree, applyDecisionTree

# parameters
k = 4
dataFile1 = "/media/sf_Google_Drive/transfer/data/data_year.csv"
#outputDir = "/media/sf_Google_Drive/transfer/model_output_year/"

# load the data, both of them
data1 = {}
columns1 = []
loadData(dataFile1, ["location", "year"], data1, columns1)

random.seed(42)
models = []
models.append({"name": "linear", "norm": NONORMALIZATION, "train": trainLinearRegression, "apply": applyLinearRegression, "data": data1, "columns": columns1, "parameters": {'intercept': True, 'normalize': True, "features": columns1}})
models.append({"name": "dtr", "norm": NONORMALIZATION, "train": trainDecisionTree, "apply": applyDecisionTree, "data": data1, "columns": columns1, "parameters": {'leaf': 10}})

evalFunctions = [rmseEval]#, correlationEval, rsquaredEval, maeEval, nmseEval, fbEval]
evalFunctionNames = ['rmse']#, 'r', 'r2', 'mae', 'nmse', 'fb']

# results
results = []

# run cross validation for all the methods
for model in models:
    random.seed(42)
    print("Running " + str(k) + "-fold X-Validation with " + model["name"] + "(norm:" + str(model["norm"]) + ")")
    result = crossValidation(k, model["data"], model["columns"], "target", model["norm"], model["train"], model["apply"], evalFunctions, model["parameters"])
    results.append([model["name"], result])

#print out results    
for result in results:
    print(str(result[0]))
    print(str(result[1]["avg"]))
    print(str(result[1]["std"]))

