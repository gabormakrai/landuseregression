from sklearn import linear_model

class Model4:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainModel4(data, columns, targetColumn):
    
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
    
    model = linear_model.LassoLars(alpha=.1)
    
    model.fit (modelData, data[targetColumn])
    
    return Model4(model, modelColumns)
    
def applyModel4(data, model):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
