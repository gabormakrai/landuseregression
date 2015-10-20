"""
Main modelling file
"""
from data import loadData
from crossvalidation import crossValidation
from eval.rmse import rmseEval
from models.model1 import trainModel1, applyModel1
import random

# parameters
k = 8
dataFile = "f:\\transfer\\data\\data.csv"
random.seed(42)
models = [{"name": "model1", "train": trainModel1, "apply": applyModel1}]

# load the data
data = {}
columns = []
loadData(dataFile, ["location", "timestamp"], data, columns)

# run cross validation for all the methods
for model in models:
    print("Running " + str(k) + "-fold X-Validation with " + model["name"])
    crossValidation(k, data, columns, "nox", model["train"], model["apply"], rmseEval)

