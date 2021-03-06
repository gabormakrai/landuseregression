from sklearn import linear_model

class LinearRegressionModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainLinearRegression(data, columns, targetColumn, parameters):
    
    modelColumns = []
    for column in columns:
        if column != targetColumn and column in parameters["features"]:
            modelColumns.append(column)
            
    modelData = []
    
    for i in range(0, len(data[targetColumn])):
        record = []
        for column in modelColumns:
            record.append(data[column][i])

        modelData.append(record)
    
    model = linear_model.LinearRegression(parameters["intercept"], parameters["normalize"], True, 1)
    
    model.fit (modelData, data[targetColumn])
    
    return LinearRegressionModel(model, modelColumns)
    
def applyLinearRegression(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
