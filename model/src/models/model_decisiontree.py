
from sklearn.tree import DecisionTreeRegressor

class DecisionTreeModel:
    def __init__(self, model, modelColumns):
        self.model = model
        self.modelColumns = modelColumns

def trainDecisionTree(data, columns, targetColumn, parameters):
    
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
        model = DecisionTreeRegressor(max_depth = parameters["depth"], random_state=42)
    elif "leaf" in parameters:
        model = DecisionTreeRegressor(min_samples_leaf = parameters["leaf"], random_state=42)
    
    model.fit (modelData, data[targetColumn])
    
    return DecisionTreeModel(model, modelColumns)
    
def applyDecisionTree(data, model, parameters):
    
    applyData = []
    
    for i in range(0, len(data[model.modelColumns[0]])):
        record = []
        for column in model.modelColumns:
            record.append(data[column][i])

        applyData.append(record)
    
    x = model.model.predict(applyData)
    
    return x
