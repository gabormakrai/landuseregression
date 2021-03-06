import math

def evalVG(targetData, predictionData):
    
    sum_target_prediction_squared = 0.0
    
    for i in range(0, len(targetData)):
        p = predictionData[i]
        o = targetData[i]
        if p == 0.0 or p < 0.0:
            p = 0.001
        if o == 0.0 or o < 0.0:
            o = 0.001
            
        sum_target_prediction_squared = sum_target_prediction_squared + math.pow(math.log(o) - math.log(p), 2.0) 
    
    avg_target_prediction_squared = sum_target_prediction_squared / float(len(targetData))
    
    value1 = math.exp(avg_target_prediction_squared)
    
    return value1

