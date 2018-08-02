import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf7.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf7.png"

data = defaultdict(lambda: defaultdict(lambda: 0.0))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if line.startswith("method"):
            continue
        s_line = line.split(',')
        n = int(s_line[0])
        ml = int(s_line[2])
        rmse = float(s_line[3])
        data[n][ml] = rmse

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(5,500)

for ml in [5000,6000,7000]:
    data1 = []
    for x1 in x:
        data1.append(data[x1][ml])
    ax.plot(x, data1, label="max_leaf_" + str(ml))

plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("Estimators")
plt.legend()

plt.savefig(OUTPUT_FILE_1)

