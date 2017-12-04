import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex1/ex1_rf2.csv"
OUTPUT_FILE_1 = "/experiments/ex1/ex1_rf2.png"

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

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

x = range(2,200)

colors = []
for i in range(0,200):
    c = hex(20 + i).split('x')[-1]
    color = "#" + c + c + c
    colors.append(color)
    
for n in range(5,200):
    data1 = []
    for x1 in x:
        data1.append(data[n][x1])
    if n % 20 == 0:
        ax.plot(x, data1, color=colors[n], label="estimator_" + str(n))
    else:
        ax.plot(x, data1, color=colors[n])

plt.xlabel("min_leaf")
plt.ylabel("RMSE (ug/m3)")
plt.legend()

plt.savefig(OUTPUT_FILE_1)
