
# calculating mae
def maeEval(targetData, predictionData):
    mae = 0.0
    for i in range(0, len(targetData)):
        mae = mae + abs(targetData[i] - predictionData[i])
    mae = mae / float(len(targetData))
    return mae
