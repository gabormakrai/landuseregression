from sklearn.svm import SVR

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
        
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    
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
