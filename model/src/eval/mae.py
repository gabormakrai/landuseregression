import math

# calculating mae
def maeEval(targetData, predictionData):
    mae = 0.0
    counter = 0
    for i in range(0, len(targetData)):
        if math.isnan(targetData[i]) or math.isnan(predictionData[i]):
            continue
        mae = mae + abs(targetData[i] - predictionData[i])
        counter = counter + 1
    mae = mae / float(counter)
    return ["mae", mae]
