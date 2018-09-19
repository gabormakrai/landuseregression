import matplotlib.pyplot as plt
from collections import defaultdict

INPUT_FILE = "/experiments/ex29/ex29_6_final.csv"
OUTPUT_FILE = "/experiments/ex29/ex29_6_final.png"

all_stations = ['71.0', '5.0', '80.0', '69.0', '15.0', '70.0', '29.0', '81.0', '52.0', '57.0', '38.0', '53.0', '31.0', '26.0', '24.0', '55.0', '67.0', '14.0', '79.0', '19.0', '91.0', '49.0', '78.0', '9.0', '43.0', '73.0', '50.0', '46.0', '16.0', '33.0', '89.0', '44.0', '7.0', '13.0', '51.0']
all_station_float = [float(s) for s in all_stations]

data_by_station = defaultdict(list)

#prediction,observation,station,model
first_line = True
with open(INPUT_FILE) as infile:
    for line in infile:
        if first_line:
            first_line = False
            continue
        line = line.rstrip()
        s_line = line.split(",")
        pred = float(s_line[0])
        obs = float(s_line[1])
        abs_error = abs(pred - obs)
        station = float(s_line[3])
        model = s_line[2]
        if model == "RFR_TW":
            data_by_station[station].append(abs_error)
            

data_to_plot = []
station_names = []
for station in all_station_float:
    station_names.append(str(int(station)))
    data_to_plot.append(data_by_station[station])

fig = plt.figure(figsize=(20, 7))
ax = fig.add_subplot(111)
  
ax.boxplot(data_to_plot, showfliers=False)
ax.set_xticklabels(station_names, rotation='vertical')
 
fig.subplots_adjust(right=0.95, left=0.075, bottom=0.15, top=0.95)
 
plt.ylabel(r'Concentration levels ($\mu$gm${}^{-3}$)')
plt.ylim(-5.0, 175.0)
 
plt.savefig(OUTPUT_FILE)
