
from sknn.mlp import Regressor, Layer
import numpy as np

class NeuralNetworkModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainNeuralNetwork(data, columns, targetColumn, parameters):

    modelColumns = []
    for column in columns:
        if column != targetColumn:
            modelColumns.append(column)
            
    modelData = []
    
    for i in range(0, len(data[targetColumn])):
        record = []
        for column in modelColumns:
            record.append(data[column][i])

        modelData.append(record)
        
    layers = []
    layers.append(Layer("Rectifier", units=60))
    for i in range(0, parameters["hidden_layers"]):
        layers.append(Layer(parameters["hidden_type"], units=parameters["hidden_neurons"]))
    layers.append(Layer("Linear"))
    model = Regressor(
        layers=layers
#             Layer("Rectifier", units=60),
#             Layer("Sigmoid", units=80),
#             Layer("Sigmoid", units=80),
#             Layer("Linear")
            ,
        learning_rate=0.01,
        n_iter=parameters["iteration"])
    
    X = np.array(modelData)
    y = np.array(data[targetColumn])
    
    model.fit(X, y)
    
    return NeuralNetworkModel(model, modelColumns)
    
def applyNeuralNetwork(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    z = np.array(applyData)
    
    x = model.model.predict(z)
    
    return x
