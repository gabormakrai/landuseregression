import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from data.data import loadData
from ex1.crossvalidation import splitDataForXValidation
from copy import deepcopy
from eval.rmse import rmseEval
from sklearn.preprocessing.data import StandardScaler
import numpy as np
from sknn.mlp import Regressor, Layer

OUTPUT_DATA_FILE = "/experiments/ex1/ex1_ann3.csv"

parametersList = []

for hiddentype in ["Sigmoid"]:
    for layers in [1]:
        for iteration in [5,6,7,8,9,10]:
            for neurons in [i*5 for i in range(1,100)]:
                parametersList.append({
                    "iteration": iteration, 
                    "hidden_neurons":neurons, 
                    "hidden_layers": layers, 
                    "hidden_type": hiddentype,
                    "learning_rate": 0.00001})

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

# load the data
data = {}
columns = []
loadData("/data/york_hour_2013.csv", ["timestamp", "atc"], data, columns)

all_features = deepcopy(columns)
all_features.remove("target")
all_features.remove("location")

all_features.remove('buildings_area')
all_features.remove('leisure_area')

output = open(OUTPUT_DATA_FILE, 'w')
output.write("iteration,neurons,layers,rmse\n")

def evalOne(parameters):
    all_obs = []
    all_pred = []
    for location in locations:
        trainX, testX, trainY, testY = splitDataForXValidation(location, "location", data, all_features, "target")
        normalizer_X = StandardScaler()
        trainX = normalizer_X.fit_transform(trainX)
        testX = normalizer_X.transform(testX)
        normalizer_Y = StandardScaler()
        trainY = normalizer_Y.fit_transform(trainY)
        testY = normalizer_Y.transform(testY)
        
        layers = []
        for _ in range(0, parameters["hidden_layers"]):
            layers.append(Layer(parameters["hidden_type"], units=parameters["hidden_neurons"]))
        layers.append(Layer("Linear"))
        model = Regressor(
            layers=layers,
            learning_rate=parameters["learning_rate"],
            n_iter=parameters["iteration"],
            random_state=42
            )
        
        X = np.array(trainX)
        y = np.array(trainY)
        
        model.fit(X, y)
        
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        prediction = normalizer_Y.inverse_transform(prediction)
        testY = normalizer_Y.inverse_transform(testY)
        
        print("location: " + str(location) + " -> " + str(rmseEval(prediction, testY)[1]))
        
        all_obs.extend(testY)
        all_pred.extend(prediction)
        
    return rmseEval(all_obs, all_pred)[1]

for p in parametersList:
    print(str(p))
    rmse = evalOne(p)
    print("\t" + str(rmse))
    output.write(str(p["iteration"]) + "," + str(p["hidden_neurons"]) + "," + str(p["hidden_layers"]) + "," + str(rmse) + "\n")
    output.flush()
    
output.close()
