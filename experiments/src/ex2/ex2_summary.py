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

methods = ["ospm", "linear_lu", "linear_all", "knn", "ann", "dt", "rf", "rf2"]

stations = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
stationNames = {2.0: "Fulford", 3.0: "Gillygate", 4.0: "Heworth", 5.0: "Holgate", 6.0: "Lawrence", 7.0: "Nunnery", 8.0: "Fishergate"}

predictions = {}
observations = {}
predictionsPerStation = defaultdict(lambda: defaultdict(list))
observationsPerStation = defaultdict(lambda: defaultdict(list))

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
        predictionsPerStation[method][l].append(p)
        observationsPerStation[method][l].append(o)
    
for method in methods:
    print("Method: " + method)
    print("\trmse: " + str(rmseEval(observations[method], predictions[method])[1]))
    print("\tmae: " + str(maeEval(observations[method], predictions[method])[1]))
    print("\tr: " + str(correlationEval(observations[method], predictions[method])[1]))
    print("\tr2: " + str(rsquaredEval(observations[method], predictions[method])[1]))
    print("\tr2: " + str(r2_score(observations[method], predictions[method])))
     
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.scatter(observations[method], predictions[method], alpha=0.1)
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.ylabel("Prediction (ug/m3)")
    plt.xlabel("Observation (ug/m3)")
    plt.savefig(OUTPUT_DIRECTORY + "ex2_" + method + ".png")
    plt.close()
 
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    for s in stations:
        ax.scatter(observationsPerStation[method][s], predictionsPerStation[method][s], alpha=0.1, label=stationNames[s])
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.ylabel("Prediction (ug/m3)")
    plt.xlabel("Observation (ug/m3)")
    leg = plt.legend()
    for lh in leg.legendHandles: 
        lh.set_alpha(1.0)
    plt.savefig(OUTPUT_DIRECTORY + "ex2_" + method + "_perstation.png")
    plt.close()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
labels = []
dataToPlot = []
for method in methods:
    labels.append(method)
    d = [abs(observations[method][i] - predictions[method][i]) for i in range(0, len(observations[method]))]
    dataToPlot.append(d)
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(labels)
plt.savefig(OUTPUT_DIRECTORY + "ex2_plot.png")
plt.close()
