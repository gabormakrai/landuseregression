import matplotlib.pyplot as plt
from data.data import loadEvalData

DATA_FILE1 = "/media/sf_lur/model_output/eval/lur.csv"
DATA_FILE2 = "/media/sf_lur/model_output/eval/ospm.csv"
DATA_FILE3 = "/media/sf_lur/model_output/eval/lur2.csv"
OUTPUT_DIR = "/media/sf_lur/model_output/eval/"

evalFunc = ["rmse", "mae", "r"]
methods = ["ospm", "linear_std", "linear", "linear_dummy", "svr", "ann", "dtr", "rfr"]
methodsName = ["OSPM", "Linear\n(only\nLU data)", "Linear\n(w/ T+W)", "Linear\n(w/ dummy)", "SVR", "ANN", "DTR", "RFR"]
yLabel = ["RMSE (ug/m3)", "MAE (ug/m3)", "r"]

data = {}
loadEvalData(DATA_FILE1, data)
loadEvalData(DATA_FILE2, data)
loadEvalData(DATA_FILE3, data)

for ev in range(0, len(evalFunc)):

    evFunc = evalFunc[ev]

    fig = plt.figure(None, figsize=(10, 12))
    ax = fig.add_subplot(111)
    
    dataToPlot = []
    
    for method in methods:
        print(method)
        d = []
        for v in data[method][evFunc]:
            d.append(v)
        print(str(d))
        dataToPlot.append(d)
    
    print(str(dataToPlot))
    ax.boxplot(dataToPlot, showfliers=False)
    ax.set_xticklabels(methodsName, rotation='vertical')
    
    plt.ylabel(yLabel[ev])
    
    plt.savefig(OUTPUT_DIR + evFunc + ".png")
    
