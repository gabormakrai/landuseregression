import matplotlib.pyplot as plt

INPUT_FILE = "/experiments/ex1/ex1_dt1.csv"
OUTPUT_FILE = "/experiments/ex1/ex1_dt1.png"

data = {"depth": [], "leaf": [], "max_leaf": []}

firstLine = True
with open(INPUT_FILE) as infile:
    for line in infile:
        line = line.rstrip()
        if line.startswith("method"):
            continue
        s_line = line.split(',')
        data[s_line[0]].append(float(s_line[2]))

fig = plt.figure(figsize=(9.36, 5.76))
ax = fig.add_subplot(111)

names = []
dataToPlot = []

x = range(2,150)

ax.plot(x, data["depth"], label="method_depth")
ax.plot(x, data["leaf"], label="method_leaf")
ax.plot(x, data["max_leaf"], label="method_max_leaf")

plt.ylabel(r'RMSE ($\mu$gm${}^{-3}$)')
plt.xlabel("parameter")
plt.legend()

plt.savefig(OUTPUT_FILE)
