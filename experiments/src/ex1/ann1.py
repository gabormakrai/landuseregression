from eval.rmse import rmseEval
from data.data import loadData
from norm import NORMALIZATION
from crossvalidation import crossValidation
import random
from models.model_ann import trainNeuralNetwork, applyNeuralNetwork

# parameters

k = 8

parametersList = []
for hiddentype in ["Linear", "Sigmoid"]:
    for layers in range(1, 5):
        for neurons in range(6, 15):
            for iteration in range(1, 5):
                parametersList.append({"iteration": iteration*500, "hidden_neurons":neurons * 10, "hidden_layers": layers, "hidden_type": hiddentype})

evalFunctions = [rmseEval]
    
# load the data
data2 = {}
columns2 = []
loadData("/media/sf_lur/data/data_hour_2013.csv", ["location", "timestamp"], data2, columns2)
 
for parameters in parametersList:
    random.seed(42)
    result = crossValidation(k, data2, columns2, "target", NORMALIZATION, trainNeuralNetwork, applyNeuralNetwork, evalFunctions, parameters)
    print(str(parameters) + " -> rmse: " + str(result["avg"]))
