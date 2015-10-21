
# calculating fractional bias
def correlationEval(targetData, predictionData):
    
    averageTarget = 0.0
    averagePrediction = 0.0
    
    for i in range(0, len(targetData)):
        averageTarget = averageTarget + targetData[i]
        averagePrediction = averagePrediction + predictionData[i]
        
    averageTarget = averageTarget / float(len(targetData))
    averagePrediction = averagePrediction / float(len(targetData))
        
    fb = (averageTarget - averagePrediction) / (0.5 * (averageTarget + averagePrediction))
    
    return fb
