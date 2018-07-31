import matplotlib.pyplot as plt
from eval.rmse import rmseEval
from eval.mae import maeEval
from eval.correlation import correlationEval
from eval.rsquared import rsquaredEval
from collections import defaultdict
from sklearn.metrics import r2_score

INPUT_DATA_FILE = "/experiments/ex29/ex29_6_final.csv"
OUTPUT_DIRECTORY = "/experiments/ex29/"

methods = ["RFR_ALL", "RFR_TW", "RFR_TWA", "RFR_combined"]

methodNames = {
    "RFR_ALL": "Random Forest\nRegression",
    "RFR_TW": "RFR+TW\nmethod",
    "RFR_TWA": "RFR+TWA\nmethod",
    "RFR_combined": "Random Forest\nensemble method",
}

methodNamesOneLine = {
    "RFR_ALL": "RFR+ALL",
    "RFR_TW": "RFR+TW",
    "RFR_TWA": "RFR+TWA",
    "RFR_combined": "RF ensemble",
}

predictions = defaultdict(list)
observations = defaultdict(list)


#prediction,observation,station,model
first_line = True
with open(INPUT_DATA_FILE) as infile:
    for line in infile:
        if first_line:
            first_line = False
            continue
        line = line.rstrip()
        s_line = line.split(",")
        pred = float(s_line[1])
        obs = float(s_line[0])
        station = float(s_line[3])
        model = s_line[2]
        predictions[model].append(pred)
        observations[model].append(obs)

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
    ax.scatter(observations[method], predictions[method], alpha=0.01)
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.ylabel("Prediction (ug/m3)")
    plt.xlabel("Observation (ug/m3)")
    plt.savefig(OUTPUT_DIRECTORY + "ex29_9_1_" + method + ".png")
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
plt.ylabel("Absolute error (ug/m3)")
plt.subplots_adjust(bottom=0.2)
plt.savefig(OUTPUT_DIRECTORY + "ex29_9_1_absolute_error_boxplot.png")
plt.close()
