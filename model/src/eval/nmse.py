import math

# calculating nmse
def nmseEval(targetData, predictionData):
    # print(targetData)
    # print(predictionData)
    nmse = 0.0
    avgTarget = 0.0
    avgPrediction = 0.0
    for i in range(0, len(targetData)):
        nmse = nmse + math.pow(targetData[i] - predictionData[i], 2.0)
        avgTarget = avgTarget + targetData[i]
        avgPrediction = avgPrediction + predictionData[i]
    
    avgTarget = avgTarget / float(len(targetData))
    avgPrediction = avgPrediction / float(len(targetData))
#     nmse1 = nmse
    nmse = nmse / (len(targetData) * avgTarget * avgPrediction)
#     if nmse > 1.0:
#         print("NMSE larger then 1.0")
#         print("avgTarget: " + str(avgTarget))
#         print("avgPrediction: " + str(avgPrediction))
#         print("original nmse: " + str(nmse1))
#         print("len(targetData): " + str(len(targetData)))
    return ["nmse", nmse]

def nmse_from_paper(targetData, predictionData):
    sum_target_prediction_squared = 0.0
    sum_target = 0.0
    sum_prediction = 0.0
    
    for i in range(0, len(targetData)):
        sum_target_prediction_squared = sum_target_prediction_squared + math.pow(targetData[i] - predictionData[i], 2.0)
        sum_target = sum_target + targetData[i]
        sum_prediction = sum_prediction + predictionData[i]
        
    avg_target_prediction_squared = sum_target_prediction_squared / float(len(targetData))
    avg_target = sum_target / float(len(targetData))
    avg_prediction = sum_prediction / float(len(targetData))
    
    return avg_target_prediction_squared / (avg_target * avg_prediction)

