import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_svm2.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_svm2.png"

# data: n_estimators,C,max_samples
data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        if firstLine:
            firstLine = False
            continue
        line = line.rstrip()
        s_line = line.split(',')
        n_estimators = int(s_line[0])
        c = int(s_line[1])
        max_samples = int(s_line[2])
        data[n_estimators][c][max_samples] = float(s_line[3])

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)
 
names = []
dataToPlot = []
 
x = range(1,79)

for samples in [i * 50 for i in range(1,111)]:
    names.append("samples_" + str(samples))
    d = []
    for x1 in x:
        d.append(data[10][x1][samples])
    dataToPlot.append(d)

colors = []
for i in range(0,130):
    c = hex(int(50 + 1.5 * i)).split('x')[-1]
    color = "#" + c + c + c
    colors.append(color)
   
for i in range(0, len(names)):
    if i == 0 or i % 10 == 9:
        ax.plot(x, dataToPlot[i], label=names[i], color=colors[i])
    else:
        ax.plot(x, dataToPlot[i], color=colors[i])
 
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("C")
plt.legend()
 
plt.savefig(OUTPUT_FILE_1)
