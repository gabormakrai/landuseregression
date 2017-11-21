import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf5.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf5.png"

data = defaultdict(lambda: defaultdict(lambda: 0.0))
firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if line.startswith("method"):
            continue
        s_line = line.split(',')
        n = int(s_line[0])
        l = int(s_line[2])
        rmse = float(s_line[3])
        data[n][l] = rmse

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(5,1000)

for l in [2,3,4]:
    data1 = []
    for x1 in x:
        data1.append(data[x1][l])
    ax.plot(x, data1, label="leaf_" + str(l))

plt.ylabel("RMSE (ug/m3)")
plt.xlabel("Estimators")
plt.legend()

plt.savefig(OUTPUT_FILE_1)

