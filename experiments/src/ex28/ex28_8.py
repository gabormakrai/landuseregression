from data.data import loadData
from collections import defaultdict
from eval.rmse import rmseEval
import matplotlib.pyplot as plt

DATA_FILE = "/experiments/ex28/ex28_7_data.csv"
OUTPUT_FILE_A = "/experiments/ex28/ex28_8_1.png"
OUTPUT_FILE_B_1 = "/experiments/ex28/ex28_8_2_tw.png"
OUTPUT_FILE_B_2 = "/experiments/ex28/ex28_8_2_lower.png"
OUTPUT_FILE_B_3 = "/experiments/ex28/ex28_8_2_upper.png"
OUTPUT_FILE_B_4 = "/experiments/ex28/ex28_8_2_combined.png"
OUTPUT_FILE_C = "/experiments/ex28/ex28_8_3.png"

all_stations = ['71.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0']

groups = [['71.0', '70.0', '38.0', '55.0', '73.0', '89.0'],
['29.0', '53.0', '67.0', '49.0', '50.0', '44.0'],
['80.0', '81.0', '31.0', '14.0', '78.0', '46.0', '7.0'],
['69.0', '52.0', '26.0', '79.0', '9.0', '16.0'],
['15.0', '57.0', '24.0', '19.0', '43.0', '33.0']]

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

absErrors = defaultdict(lambda: defaultdict(list))

rmse_tw = rmseEval(data["obs"], data["pred_tw"])[1]
rmse_lower = rmseEval(data["obs"], data["pred_tw_lower"])[1]
rmse_upper = rmseEval(data["obs"], data["pred_tw_upper"])[1]
rmse_combined = rmseEval(data["obs"], data["pred_combined"])[1]

print("rmse_tw: " + str(rmse_tw))
print("rmse_lower: " + str(rmse_lower))
print("rmse_upper: " + str(rmse_upper))
print("rmse_combined: " + str(rmse_combined))

for i in range(0, len(data["obs"])):
    location = data["location"][i]
    obs = data["obs"][i]
    pred_TW = data["pred_tw"][i]
    pred_lower = data["pred_tw_lower"][i]
    pred_upper = data["pred_tw_upper"][i]
    pred_combined = data["pred_combined"][i]
     
    absErrors["tw"][str(location)].append(abs(obs - pred_TW))
    absErrors["lower"][str(location)].append(abs(obs - pred_lower))
    absErrors["upper"][str(location)].append(abs(obs - pred_upper))
    absErrors["combined"][str(location)].append(abs(obs - pred_combined))

fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

for group in range(0, 5):
    for station in groups[group]:
        names.append(str(int(float(station))) + " TW")
        dataToPlot.append(absErrors["tw"][station])
        names.append(str(int(float(station))) + " Combined")
        dataToPlot.append(absErrors["combined"][station])

ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')

plt.title("Data T")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 110.0)

plt.savefig(OUTPUT_FILE_A)
 
# 2 tw
fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)
names = []
dataToPlot = []
for station in all_stations:
        names.append(str(int(float(station))) + " TW")
        dataToPlot.append(absErrors["tw"][station])
 
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.title("RFR+TW prediction's absolute error")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 110.0)
plt.savefig(OUTPUT_FILE_B_1)
 
# 2 lower
fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)
names = []
dataToPlot = []
for station in all_stations:
        names.append(str(int(float(station))) + " lower")
        dataToPlot.append(absErrors["lower"][station])
 
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.title("RFR+TW_lower prediction's absolute error")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 150.0)
plt.savefig(OUTPUT_FILE_B_2)
 
# 2 upper
fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)
names = []
dataToPlot = []
for station in all_stations:
        names.append(str(int(float(station))) + " upper")
        dataToPlot.append(absErrors["upper"][station])
 
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.title("RFR+TW_upper prediction's absolute error")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 110.0)
plt.savefig(OUTPUT_FILE_B_3)
 
# 2 combined
fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)
names = []
dataToPlot = []
for station in all_stations:
        names.append(str(int(float(station))) + " combined")
        dataToPlot.append(absErrors["combined"][station])
 
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.title("RFR+TW_combined prediction's absolute error")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 110.0)
plt.savefig(OUTPUT_FILE_B_4)
 
# 3
fig = plt.figure(figsize=(24, 10))
ax = fig.add_subplot(111)
names = []
dataToPlot = []
for station in all_stations:
        names.append(str(int(float(station))) + " TW")
        dataToPlot.append(absErrors["tw"][station])
        names.append(str(int(float(station))) + " Combined")
        dataToPlot.append(absErrors["combined"][station])
 
ax.boxplot(dataToPlot, showfliers=False)
ax.set_xticklabels(names, rotation='vertical')
plt.title("RFR_TW and RFR+TW_combined prediction's absolute error")
plt.ylabel("Absolute errors (ug/m3)")
plt.ylim(-5.0, 110.0)
plt.savefig(OUTPUT_FILE_C)
