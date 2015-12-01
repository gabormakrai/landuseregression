from sklearn.neighbors.regression import KNeighborsRegressor

class NearestNeighborsModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainNearestNeighbors(data, columns, targetColumn, parameters):
    
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
        
    model = KNeighborsRegressor(weights = parameters["weights"], n_neighbors = parameters["neighbors"], p = parameters["p"])
    
    model.fit (modelData, data[targetColumn])
    
    return NearestNeighborsModel(model, modelColumns)
    
def applyNearestNeighbors(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
