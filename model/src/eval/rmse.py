import math

# calculating rmse
def rmseEval(targetData, predictionData):
    
    # print(targetData)
    # print(predictionData)
    
    rmse = 0.0
    counter = 0
    for i in range(0, len(targetData)):
        if math.isnan(targetData[i]) or math.isnan(predictionData[i]):
            continue
        rmse = rmse + math.pow(targetData[i] - predictionData[i], 2.0)
        counter = counter + 1
    rmse = math.sqrt(rmse / float(counter))
    return ["rmse", rmse]
