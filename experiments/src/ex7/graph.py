import matplotlib.pyplot as plt

def doLineChart(fileName, title, xAxis, yAxis, weeklyObs, weeklyPred):
    
    obs1 = weeklyObs["6.0"]
    obs2 = weeklyObs["7.0"]
    pred1 = weeklyPred["6.0"]
    pred2 = weeklyPred["7.0"]
    
#     for i in range(0, len(obs1)):
#         print(str(obs1[i]) + " -" + str(pred1[i]))
    
    index = []
    for i in range(0, len(obs1)):
        index.append(i)
        
    fig = plt.figure(None, figsize=(10, 10))
    ax = fig.add_subplot(111)
    
    ax.plot(index, pred1, '-', color="b", label="Prediction - Lawrence")
    ax.plot(index, pred2, '-', color="y", label="Prediction - Nunnery")
    
    ax.plot(index, obs1, '--', color="r", label="Observed - Lawrence")
    ax.plot(index, obs2, '--', color="g", label="Observed - Nunnery")
     
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    ax.legend()
    
#     plt.xticks(index + (0.5 / 2), names)
     
    plt.margins(0.04, 0.04)
 
    plt.savefig(fileName)

