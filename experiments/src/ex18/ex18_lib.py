import matplotlib.pyplot as plt
from crossvalidation import splitDataForXValidation
from sklearn.ensemble.forest import RandomForestRegressor
from eval.rmse import rmseEval

def plotArray(fileName, title, xAxis, yAxis, names, data):
    index = []
    for i in range(0, len(data[0])):
        index.append(i)
        
    fig = plt.figure(None, figsize=(12, 10))
    ax = fig.add_subplot(111)
    
    for i in range(0, len(names)):
        ax.plot(index, data[i], '.', label=names[i])
     
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)
    plt.margins(0.04, 0.04)
    plt.legend(loc='center left')

    plt.savefig(fileName)
        
def doPrediction(locations, data, columns, features, columns2, outputFileName):
    predictionData = {}
    for c in columns2:
        predictionData[c] = [] 
    
    # modelling
    for location in locations:
        trainX, testX, trainY, testY, dataY = splitDataForXValidation(location, "location", data, features, columns, "target")
        print("\tT+W #train: " + str(len(trainY)) + ", #test:" + str(len(testY)))
        model = RandomForestRegressor(min_samples_leaf = 2, n_estimators = 650, n_jobs = -1, random_state=42)
        model.fit(trainX, trainY)
        prediction = model.predict(testX)
        rmse = rmseEval(testY, prediction)[1]
        print("\trmse: " + str(rmse))
        
        for c in columns2:
            if c == 'prediction':
                predictionData[c].extend(prediction)
            else:
                predictionData[c].extend(dataY[c])
    
    for c in predictionData:
        print("\t" + c + " -> #" + str(len(predictionData[c])))
    
    rmse = rmseEval(predictionData['target'], predictionData['prediction'])[1]
    print("overall RMSE: " + str(rmse))
    
    print("Writing out results...")
    
    output = open(outputFileName, 'w')
    output.write(','.join([str(x) for x in columns2]))
    output.write("\n")
    
    for i in range(0, len(predictionData['target'])):
        output.write(str(predictionData[columns2[0]][i]))
        for j in range(1, len(columns2)):
            output.write(",")
            output.write(str(predictionData[columns2[j]][i]))
        output.write("\n")
    
    output.close()
    
    print("Done...")
    
def doBoxplot(fileName, title, yAxis, showFliers, data, names):
    
#    fig = plt.figure(None, figsize=(12, 10))
    fig = plt.figure(None, figsize=(13, 8))
    
    ax = fig.add_subplot(111)

    ax.boxplot(data, showfliers=showFliers)
    
    ax.set_xticklabels(names)#, rotation='vertical')
    
    plt.ylabel(yAxis)
    
    #plt.title(title)
    
    plt.savefig(fileName)
    
    