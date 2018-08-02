import matplotlib.pyplot as plt
from data.data import loadData
from eval.rmse import rmseEval
from eval.mae import maeEval
from eval.correlation import correlationEval
from eval.rsquared import rsquaredEval
from collections import defaultdict
from sklearn.metrics import r2_score

INPUT_DATA_DIRECTORY = "/experimntes/ex2/"
OUTPUT_DIRECTORY = "/experiments/ex2/"

methods = ["ospm", "linear_lu", "linear_all", "knn", "ann", "svm", "dt", "rf"]

methodNames = {
    "ospm": "OSPM\nmethod",
    "linear_lu": "Standard\nLUR",
    "linear_all": "Linear\nRegression",
    "knn": "Nearest Neighour\nRegression",
    "svm": "Support Vector\nRegression",
    "ann": "Neural Network\nRegression",
    "dt": "Decision Tree\nRegression",
    "rf": "Random Forest\nRegression"
}

methodNamesOneLine = {
    "linear_lu": "Standard LUR",
    "linear_all": "Linear Regression",
    "knn": "Nearest Neighour Regression",
    "svm": "Support Vector Regression",
    "ann": "Neural Network Regression",
    "dt": "Decision Tree Regression",
    "rf": "Random Forest Regression"
}

stations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
stationNames = {2.0: "Fulford", 3.0: "Gillygate", 4.0: "Heworth", 5.0: "Holgate", 6.0: "Lawrence", 7.0: "Nunnery", 8.0: "Fishergate"}

predictions = {}
observations = {}
predictionsPerStation = defaultdict(lambda: defaultdict(list))
observationsPerStation = defaultdict(lambda: defaultdict(list))
predictionsNormal = defaultdict(list)
observationsNormal = defaultdict(list)

for method in methods:
    d = {}
    columns = []
    loadData("/experiments/ex2/ex2_" + method + ".csv", [], d, columns)
    predictions[method] = d["prediction"]
    observations[method] = d["observation"]
    for i in range(0, len(d["prediction"])):
        p = d["prediction"][i]
        o = d["observation"][i]
        l = d["location"][i]
        if method == 'svm' and l == 6.0:
            continue
        predictionsPerStation[method][l].append(p)
        observationsPerStation[method][l].append(o)
        predictionsNormal[method].append(p)
        observationsNormal[method].append(o)

rmseLevels = {}
maeLevels = {}
rLevels = {}
    
for method in methods:
    print("Method: " + method)
    rmse = rmseEval(observations[method], predictions[method])[1]
    print("\trmse: " + str(rmse))
    mae = maeEval(observations[method], predictions[method])[1]
    print("\tmae: " + str(mae))
    r = correlationEval(observations[method], predictions[method])[1]
    print("\tr: " + str(r))
    print("\tr2: " + str(rsquaredEval(observations[method], predictions[method])[1]))
    print("\tr2: " + str(r2_score(observations[method], predictions[method])))
    
    rmseLevels[method] = str(rmse)[0:5]
    maeLevels[method] = str(mae)[0:5]
    rLevels[method] = str(r)[0:4]
      
    fig = plt.figure(figsize=(5.76, 5.76))
    ax = fig.add_subplot(111)
    ax.scatter(observationsNormal[method], predictionsNormal[method], alpha=0.1)
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.ylabel(r'Prediction ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Observation ($\mu$gm${}^{-3}$)')
    plt.savefig(OUTPUT_DIRECTORY + "ex2_" + method + ".png")
    plt.close()
  
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    for s in stations:
        ax.scatter(observationsPerStation[method][s], predictionsPerStation[method][s], alpha=0.1, label=stationNames[s])
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.ylabel(r'Prediction ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Observation ($\mu$gm${}^{-3}$)')
    leg = plt.legend()
    for lh in leg.legendHandles: 
        lh.set_alpha(1.0)
    plt.savefig(OUTPUT_DIRECTORY + "ex2_" + method + "_perstation.png")
    plt.close()
    
    if method != "ospm":
        fig = plt.figure(figsize=(5.76, 5.76))
        ax = fig.add_subplot(111)
        ax.scatter(observationsNormal["ospm"], predictionsNormal["ospm"], alpha=0.02, label="OSPM",c='g')
        ax.scatter(observationsNormal[method], predictionsNormal[method], alpha=0.02, label=methodNamesOneLine[method],c='r')
        plt.xlim(0,150)
        plt.ylim(0,150)
        plt.ylabel(r'Prediction ($\mu$gm${}^{-3}$)')
        plt.xlabel(r'Observation ($\mu$gm${}^{-3}$)')
        leg = plt.legend()
        for lh in leg.legendHandles: 
            lh.set_alpha(1.0)
        plt.savefig(OUTPUT_DIRECTORY + "ex2_" + method + "_vs_ospm.png")
        plt.close()

fig = plt.figure(figsize=(13.0, 8.0))
ax = fig.add_subplot(111)
labels = []
dataToPlot = []
for method in methods:
    label = methodNames[method]
    label = label + "\n" + "RMSE:" + rmseLevels[method] 
    label = label + "\n" + "MAE:" + maeLevels[method] 
    label = label + "\n" + "r:" + rLevels[method] 
    labels.append(label)
    d = [abs(observations[method][i] - predictions[method][i]) for i in range(0, len(observations[method]))]
    dataToPlot.append(d)
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(labels)
plt.ylabel(r'Absolute error ($\mu$gm${}^{-3}$)')
plt.subplots_adjust(bottom=0.2)
plt.savefig(OUTPUT_DIRECTORY + "ex2_absolute_error_boxplot.png")
plt.close()
