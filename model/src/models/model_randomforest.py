from sklearn.ensemble.forest import RandomForestRegressor

class RandomForestModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainRandomForest(data, columns, targetColumn, parameters):
    
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
    if "depth" in parameters:
        model = RandomForestRegressor(max_depth = parameters["depth"], n_estimators = parameters["estimators"], n_jobs = -1)
    elif "leaf" in parameters:
        model = RandomForestRegressor(min_samples_leaf = parameters["leaf"], n_estimators = parameters["estimators"], n_jobs = -1)
    
    model.fit (modelData, data[targetColumn])
    
    return RandomForestModel(model, modelColumns)
    
def applyRandomForest(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
