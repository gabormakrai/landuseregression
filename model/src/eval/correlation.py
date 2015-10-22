import math

# calculating correlation
def correlationEval(targetData, predictionData):
    
    averageTarget = 0.0
    averagePrediction = 0.0
    
    for i in range(0, len(targetData)):
        averageTarget = averageTarget + targetData[i]
        averagePrediction = averagePrediction + predictionData[i]
        
    averageTarget = averageTarget / float(len(targetData))
    averagePrediction = averagePrediction / float(len(targetData))
    
    r = 0.0
    varianceTarget = 0.0
    variancePrediction = 0.0
    
    for i in range(0, len(targetData)):
        r = r + (targetData[i] - averageTarget) * (predictionData[i] - averagePrediction)
        varianceTarget = varianceTarget + math.pow(targetData[i] - averageTarget, 2.0)
        variancePrediction = variancePrediction + math.pow(predictionData[i] - averagePrediction, 2.0)
    
    stddevTarget = math.sqrt(varianceTarget)
    stddevPrediction = math.sqrt(variancePrediction)
    
    r = r / (stddevTarget * stddevPrediction)
    
    return ["r", r]
