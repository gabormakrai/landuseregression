"""
Main modelling file
"""
import random
from data import loadData
from crossvalidation import crossValidation
from eval.rmse import rmseEval
from models.model1 import trainModel1, applyModel1
from models.model2 import trainModel2, applyModel2
from models.model3 import trainModel3, applyModel3
from models.model4 import trainModel4, applyModel4
from models.model5 import trainModel5, applyModel5
from models.model6 import trainModel6, applyModel6
from norm import NORMALIZATION
from norm import NONORMALIZATION
from eval.correlation import correlationEval
from eval.mae import maeEval
from eval.fb import fbEval

# parameters
k = 8
dataFile = "f:\\transfer\\data\\data.csv"
random.seed(42)
models = []
models.append({"name": "model1", "norm": NONORMALIZATION, "train": trainModel1, "apply": applyModel1})
models.append({"name": "model2", "norm": NONORMALIZATION, "train": trainModel2, "apply": applyModel2})
models.append({"name": "model3", "norm": NONORMALIZATION, "train": trainModel3, "apply": applyModel3})
models.append({"name": "model4", "norm": NONORMALIZATION, "train": trainModel4, "apply": applyModel4})
models.append({"name": "model5", "norm": NONORMALIZATION, "train": trainModel5, "apply": applyModel5})
models.append({"name": "model6", "norm": NONORMALIZATION, "train": trainModel6, "apply": applyModel6})

evalFunctions = [rmseEval, correlationEval, maeEval, fbEval]

# load the data
data = {}
columns = []
loadData(dataFile, ["location", "timestamp"], data, columns)

# run cross validation for all the methods
for model in models:
    print("Running " + str(k) + "-fold X-Validation with " + model["name"] + "(norm:" + str(model["norm"]) + ")")
    crossValidation(k, data, columns, "nox", model["norm"], model["train"], model["apply"], evalFunctions)

