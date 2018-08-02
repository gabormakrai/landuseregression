import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf4.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf4.png"

data = defaultdict(lambda: defaultdict(lambda: 0.0))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if line.startswith("method"):
            continue
        s_line = line.split(',')
        n = int(s_line[0])
        d = int(s_line[2])
        rmse = float(s_line[3])
        data[n][d] = rmse

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(5,500)
    
for d in [10,15,20,25,30]:
    data1 = []
    for x1 in x:
        data1.append(data[x1][d])
    ax.plot(x, data1, label="depth_"+str(d))

plt.legend()
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("Estimators")

plt.savefig(OUTPUT_FILE_1)
