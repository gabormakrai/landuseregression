import matplotlib.pyplot as plt
from data.data import loadData
from eval.rmse import rmseEval
from eval.mae import maeEval
from eval.correlation import correlationEval
from eval.rsquared import rsquaredEval
from collections import defaultdict
from sklearn.metrics import r2_score
from eval.fac2 import fac2Eval
from eval.mg import mgEval
from eval.nmse import nmse_from_paper
from eval.fb import fbEval
from eval.random_scatter import evalRandomScatter
from eval.vg import evalVG

INPUT_DATA_DIRECTORY = "/experimntes/ex7/"
OUTPUT_DIRECTORY = "/experiments/ex7/"

methods = ["ospm", "rf", "rf_tw"]

methodNames = {
    "ospm": "OSPM\nmethod",
    "rf": "Random Forest\nRegression",
    "rf_tw": "RFR\nUsing only TW data"
}

methodNamesOneLine = {
    "linear_lu": "Standard LUR",
    "rf": "Random Forest Regression",
    "rf_tw": "RFR+TW"
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
    loadData("/experiments/ex7/ex7_" + method + ".csv", [], d, columns)
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
fac2Levels = {}
nmseLevels = {}
fbLevels = {}
rsLevels = {}
mgLevels = {}
vgLevels = {}
    
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
    fac2 = fac2Eval(observations[method], predictions[method])
    print("\tfac2: " + str(fac2))
    print("\tmg: " + str(mgEval(observations[method], predictions[method])))
    nmse = nmse_from_paper(observations[method], predictions[method])
    print("\tnmse: " + str(nmse))
    fb = fbEval(observations[method], predictions[method])[1] 
    print("\tfb: " + str(fb))
    rs = evalRandomScatter(observations[method], predictions[method])
    print("\trandom_scatter: " + str(rs))
    mg = mgEval(observations[method], predictions[method])
    print("\tmeab bias (mg): " + str(mg))
    vg = evalVG(observations[method], predictions[method])
    print("\tvg: " + str(vg))
    
    rmseLevels[method] = str(rmse)[0:4]
    maeLevels[method] = str(mae)[0:4]
    rLevels[method] = str(r)[0:4]
    fac2Levels[method] = str(fac2)[0:4]
    nmseLevels[method] = str(nmse)[0:4]
    mgLevels[method] = str(mg)[0:4]
    vgLevels[method] = str(vg)[0:4]
    if abs(fb) < 0.01:
        fbLevels[method] = "0.00"     
    elif fb < 0.0:
        fbLevels[method] = str(fb)[0:5]
    else:
        fbLevels[method] = str(fb)[0:4]
    if fbLevels[method] == '-0.00':
        fbLevels[method] = '0.00'
    rsLevels[method] = str(rs)[0:4]
      
    fig = plt.figure(figsize=(5.76, 5.76))
    ax = fig.add_subplot(111)
    ax.scatter(observationsNormal[method], predictionsNormal[method], alpha=0.1, label="Prediction-observation pairs")
    ax.plot([0,150], [0, 75], color='red', label="FAC2 lines")
    ax.plot([0,75], [0, 150], color='red')
    plt.xlim(0,150)
    plt.ylim(0,150)
    plt.ylabel(r'Prediction ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Observation ($\mu$gm${}^{-3}$)')
    plt.text(100, 143, "RMSE: " + rmseLevels[method])
    plt.text(127, 143, "$\mu$gm${}^{-3}$")
    plt.text(100, 137, "NMSE: " + nmseLevels[method])
    plt.text(100, 131, "R: " + rLevels[method])
    plt.text(100, 125, "FAC2: " + fac2Levels[method])
    plt.text(100, 119, "FB: " + fbLevels[method])
    plt.text(100, 113, "MG: " + mgLevels[method])
    plt.text(100, 107, "VG: " + vgLevels[method])
       
    leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
       
    for lh in leg.legendHandles: 
        lh.set_alpha(1.0)
           
    plt.savefig(OUTPUT_DIRECTORY + "ex7_" + method + ".png")
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
    plt.savefig(OUTPUT_DIRECTORY + "ex7_" + method + "_perstation.png")
    plt.close()
      
    if method != "ospm":
        fig = plt.figure(figsize=(5.76, 5.76))
        ax = fig.add_subplot(111)
        ax.scatter(observationsNormal["ospm"], predictionsNormal["ospm"], alpha=0.02, label="OSPM",c='g')
        ax.scatter(observationsNormal[method], predictionsNormal[method], alpha=0.02, label=methodNamesOneLine[method],c='r')
        plt.xlim(0,150)
        plt.ylim(0,150)
        plt.ylabel("Prediction (ug/m3)")
        plt.xlabel("Observation (ug/m3)")
        leg = plt.legend()
        for lh in leg.legendHandles: 
            lh.set_alpha(1.0)
        plt.savefig(OUTPUT_DIRECTORY + "ex7_" + method + "_vs_ospm.png")
        plt.close()

fig = plt.figure(figsize=(13.0 * 0.75, 8.0 * 0.75))
ax = fig.add_subplot(111)
labels = []
dataToPlot = []
for method in methods:
    label = methodNames[method]
    label = label + "\n" + "RMSE:" + rmseLevels[method] #+ "$\mu$gm${}^{-3}$" 
    label = label + "\n" + "MAE:" + maeLevels[method] #+ "$\mu$gm${}^{-3}$"
    label = label + "\n" + "NMSE:" + nmseLevels[method]
    label = label + "\n" + "R:" + rLevels[method]
    label = label + "\n" + "FB:" + fbLevels[method]
    label = label + "\n" + "MG:" + mgLevels[method]
    label = label + "\n" + "VG:" + vgLevels[method]
    label = label + "\n" + "FAC2:" + fac2Levels[method]
    labels.append(label)
    d = [abs(observations[method][i] - predictions[method][i]) for i in range(0, len(observations[method]))]
    dataToPlot.append(d)
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(labels)
plt.ylabel(r'Absolute error ($\mu$gm${}^{-3}$)')
plt.subplots_adjust(bottom=0.3)
plt.text(1.15, -9.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(1.13, -11.3, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(2.15, -9.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(2.13, -11.3, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(3.15, -9.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(3.13, -11.3, "$\mu$gm${}^{-3}$", fontsize=8)
plt.savefig(OUTPUT_DIRECTORY + "ex7_absolute_error_boxplot.png")
plt.close()
