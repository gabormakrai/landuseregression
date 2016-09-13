import math

def raeEval(targetData, predictionData):
    rae = []
    
    for i in range(len(targetData)):
        if targetData[i] < 0.01:
            rae.append(0.0)
        else:
            e = abs(targetData[i] - predictionData[i]) / targetData[i]
            rae.append(e)

    return ["rae", rae]



# calculating rmse
def rmseEval(targetData, predictionData):
    # print(targetData)
    # print(predictionData)
    rmse = 0.0
    for i in range(0, len(targetData)):
        rmse = rmse + math.pow(targetData[i] - predictionData[i], 2.0)
    rmse = math.sqrt(rmse / float(len(targetData)))
    return ["rmse", rmse]
