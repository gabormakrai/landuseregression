import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf1.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf1.png"

data = defaultdict(list)

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if line.startswith("method"):
            continue
        s_line = line.split(',')
        data[int(s_line[0])].append(float(s_line[3]))

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(2,50)

colors = []
for i in range(0,200):
    c = hex(17 + i).split('x')[-1]
    color = "#" + c + c + c
    colors.append(color)
    
for n in range(5,200):
    if n % 20 == 0:
        ax.plot(x, data[n], color=colors[n], label="estimator_" + str(n))
    else:
        ax.plot(x, data[n], color=colors[n])

plt.xlabel("depth")
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.legend()

plt.savefig(OUTPUT_FILE_1)

