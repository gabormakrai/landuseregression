import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_ann2.csv"
OUTPUT_FILE = "/experiments/ex1/ex1_ann2.png"

data = defaultdict(lambda: defaultdict(lambda: 0.0))

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        if firstLine:
            firstLine = False
            continue
        line = line.rstrip()
        s_line = line.split(',')
        data[int(s_line[0])][int(s_line[1])] = float(s_line[3])

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = [i*5 for i in range(1,100)]

for iteration in [5, 6, 7, 8, 9, 10, 11]:
    names.append("iteration_" + str(iteration))
    d = []
    for x1 in x:
        d.append(data[iteration][x1])
    dataToPlot.append(d)

colors = []
for i in range(0,10):
    c = hex(int(50 + 15 * i)).split('x')[-1]
    color = "#" + c + c + c
    colors.append(color)
   
for i in range(0, len(names)):
    ax.plot(x, dataToPlot[i], label=names[i], color=colors[i])
 
plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("neurons")
plt.legend()
 
plt.savefig(OUTPUT_FILE)
