from data.data import loadData
from ex25.ex25_lib import getXYFromData
from collections import defaultdict
from eval.rmse import rmseEval
from sklearn.tree.tree import DecisionTreeClassifier
from sklearn import tree

DATA_FILE = "/experiments/ex25/data.csv"
OUTPUT_TREE_FILE = '/experiments/ex25/tree.dot'
data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

all_features = ['hour', 'day_of_week', 'month', 'bank_holiday', 'race_day', 'winddirection', 'windspeed', 'temperature', 'rain', 'pressure', 'atc', 'lane_length', 'length', 'landuse_area', 'leisure_area', 'buildings_area', 'buildings_number']
top16tags = ['TWL', 'TW', 'TWA', 'AL', 'WA', 'A' , 'W', 'TA', 'TL', 'TWB', 'TWAL', 'WL', 'TR', 'WAR', 'WAL', 'TWR'] 
top16preds = ["pred_" + tag for tag in top16tags]

columns = all_features # + top16preds
print(str(columns))

X, Y = getXYFromData(data, columns, "target")

bestPossibleY = []

labelY = []
for i in range(0, len(Y)):
    bestAbs = abs(Y[i] - data["pred_TW"][i])
    bestIndex = 1 # TW
    bestP = data["pred_TW"][i]
    for j in range(0, len(top16tags)):
        modelAbs = abs(Y[i] - data["pred_" + top16tags[j]][i])
        if modelAbs < bestAbs:
            bestAbs = modelAbs
            bestIndex = j
            bestP = data["pred_" + top16tags[j]][i]
    labelY.append(bestIndex)
    bestPossibleY.append(bestP)

print("Label Y stat:")
labelYStat = defaultdict(lambda: 0)
for ly in labelY:
    labelYStat[ly] = labelYStat[ly] + 1
for i in range(0, 16):
    print("\tindex " + str(i) + ": " + str(labelYStat[i]))

model_to_show = DecisionTreeClassifier(random_state=42, max_depth=5)
model = DecisionTreeClassifier(random_state=42, max_depth=30)
# model = RandomForestClassifier(n_estimators=25, random_state=42) 
model.fit(X, labelY)
model_to_show.fit(X, labelY)

tree.export_graphviz(model_to_show, out_file=OUTPUT_TREE_FILE, feature_names=columns, label='none') 

predY = model.predict(X)

print("Pred Y stat:")
predYStat = defaultdict(lambda: 0)
for py in predY:
    predYStat[py] = predYStat[py] + 1
for i in range(0, 16):
    print("\tindex " + str(i) + ": " + str(predYStat[i]))

prediction = []
for i in range(0, len(Y)):
    p = data["pred_" + top16tags[predY[i]]][i]
    prediction.append(p)

rmse = rmseEval(Y, data["pred_TW"])[1]
print("TW Rmse: " + str(rmse))
rmse = rmseEval(Y, bestPossibleY)[1]
print("Best possible rmse: " + str(rmse))
rmse = rmseEval(Y, prediction)[1]
print("Rmse: " + str(rmse))

