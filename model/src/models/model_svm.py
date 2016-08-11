from sklearn.svm import SVR
from sklearn.ensemble.bagging import BaggingRegressor

class SVMModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainSVM(data, columns, targetColumn, parameters):
    
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
    
    #model = BaggingRegressor(base_estimator=SVR(kernel='rbf', C=1e4,cache_size=5000), max_samples=4000,n_estimators=10, verbose=0, n_jobs=-1)
    model = BaggingRegressor(base_estimator=SVR(kernel='rbf', C=parameters["C"], cache_size=5000), max_samples=parameters["max_samples"],n_estimators=parameters["n_estimators"], verbose=0, n_jobs=-1)
    
    model.fit (modelData, data[targetColumn])
    
    return SVMModel(model, modelColumns)
    
def applySVM(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
