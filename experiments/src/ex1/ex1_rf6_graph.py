import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf6.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf6.png"

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

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(2,15000,10)

for n in [20,40,60]:
    data1 = []
    for x1 in x:
        data1.append(data[n][x1])
    ax.plot(x, data1)

plt.title("Title")
plt.ylabel("yLabel")

plt.savefig(OUTPUT_FILE_1)

