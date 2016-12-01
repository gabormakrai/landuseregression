from math import floor

def maeDistribution(targetData, predictionData,maxMae):
    mae = []
    for i in range(0, maxMae):
        mae.append(0)
    
    for i in range(len(targetData)):
        e = abs(targetData[i] - predictionData[i])
        if e > maxMae:
            continue
        index = floor(e)
        mae[index] = mae[index] + 1

    return ["maeDistribution", mae]

def maeDistribution2(targetData, predictionData,maxMae):
    mae = []
    for i in range(0, maxMae * 2 + 1):
        mae.append(0)
    
    for i in range(len(targetData)):
        e = targetData[i] - predictionData[i]
        if e < 0.0 and e < -maxMae or e > 0.0 and e > maxMae:
            continue
        index = floor(e) + maxMae
        mae[index] = mae[index] + 1

    return ["maeDistribution2", mae]

def reDistribution(targetData, predictionData):
    re = []
    for i in range(0,300):
        re.append(0)
    
    for i in range(len(targetData)):
        if (targetData[i] < 0.0001):
            continue
        e = abs(targetData[i] - predictionData[i]) / targetData[i]
        index = int(floor(e * 100.0))
        if index > 299:
            continue
        re[index] = re[index] + 1

    return ["reDistribution", re]

def reDistribution2(targetData, predictionData):
    re = []
    for i in range(-300,300):
        re.append(0)
    
    for i in range(len(targetData)):
        if (targetData[i] < 0.0001):
            continue
        e = (predictionData[i] - targetData[i]) / targetData[i]
        index = int(floor(e * 100.0))
        if index > 299 or index < -299:
            continue
        re[index+300] = re[index+300] + 1

    return ["reDistribution2", re]
