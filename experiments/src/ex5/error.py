
def raeEval(targetData, predictionData):
    rae = []
    
    for i in range(len(targetData)):
        if targetData[i] < 0.01:
            rae.append(0.0)
        else:
            e = abs(targetData[i] - predictionData[i]) / targetData[i]
            rae.append(e)

    return ["rae", rae]

