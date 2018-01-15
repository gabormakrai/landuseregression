from data.data import loadData
from ex2.crossvalidation import splitDataForXValidation
from copy import deepcopy
from sklearn.preprocessing.data import StandardScaler
import numpy as np
from sknn.mlp import Regressor, Layer

OUTPUT_DATA_FILE = "/experiments/ex2/ex2_ann.csv"

locations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

parameters = {"iteration": 7, 
              "hidden_neurons":230, 
              "hidden_layers": 1, 
              "hidden_type": "Sigmoid",
              "learning_rate": 0.00001}

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
output.write("location,observation,prediction\n")

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
        
    for i in range(0, len(testY)):
        output.write(str(location))
        output.write(",")
        output.write(str(testY[i]))
        output.write(",")
        output.write(str(prediction[i][0]))
        output.write("\n")
        
output.close()        
