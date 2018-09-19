import matplotlib.pyplot as plt
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

INPUT_DATA_FILE = "/experiments/ex29/ex29_7_final.csv"
OUTPUT_DIRECTORY = "/experiments/ex29/"

methods = ["RFR_TW", "TW_lower", "TW_upper", "RFR_combined"]

methodNames = {
    "RFR_TW": "RFR+TW\nmethod",
    "TW_lower": "RFR+TW\nlower method",
    "TW_upper": "RFR+TW\nupper method",
    "RFR_combined": "Random Forest\nensemble method",
}

methodNamesOneLine = {
    "RFR_TW": "RFR+TW",
    "TW_lower": "RFR+TW_lower",
    "TW_upper": "RFR+TW_upper",
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
    ax.scatter(observations[method], predictions[method], alpha=0.1, label="Prediction-observation pairs")
    ax.plot([0,300], [0, 150], color='red', label="FAC2 lines")
    ax.plot([0,150], [0, 300], color='red')
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.ylabel(r'Prediction ($\mu$gm${}^{-3}$)')
    plt.xlabel(r'Observation ($\mu$gm${}^{-3}$)')
     
    plt.text(100*2, 143*2, "RMSE: " + rmseLevels[method])
    plt.text(127*2, 143*2, "$\mu$gm${}^{-3}$")
    plt.text(100*2, 137*2, "NMSE: " + nmseLevels[method])
    plt.text(100*2, 131*2, "R: " + rLevels[method])
    plt.text(100*2, 125*2, "FAC2: " + fac2Levels[method])
    plt.text(100*2, 119*2, "FB: " + fbLevels[method])
    plt.text(100*2, 113*2, "MG: " + mgLevels[method])
    plt.text(100*2, 107*2, "VG: " + vgLevels[method])
               
    leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
        
    for lh in leg.legendHandles: 
        lh.set_alpha(1.0)
            
    plt.savefig(OUTPUT_DIRECTORY + "ex29_9_2_" + method + ".png")
    plt.close()

fig = plt.figure(figsize=(13.0, 8.0))
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
plt.text(1.15, -12.2, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(1.13, -15.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(2.15, -12.2, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(2.13, -15.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(3.15, -12.2, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(3.13, -15.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(4.15, -12.2, "$\mu$gm${}^{-3}$", fontsize=8)
plt.text(4.13, -15.1, "$\mu$gm${}^{-3}$", fontsize=8)
plt.savefig(OUTPUT_DIRECTORY + "ex29_9_2_absolute_error_boxplot.png")
plt.close()
