from sknn.mlp import Regressor, Layer

class NeuralNetworkModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainNeuralNetwork(data, columns, targetColumn, params):
    
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
    
    model = Regressor(
    layers=[
        Layer("Rectifier", units=100),
        Layer("Linear")], 
    learning_rate=0.02, n_iter=100)
    
    model.fit (modelData, data[targetColumn])
    
    return NeuralNetworkModel(model, modelColumns)
    
def applyNeuralNetwork(data, model):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x

