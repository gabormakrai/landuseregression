from matplotlib import pyplot
from scipy.optimize.minpack import leastsq
import numpy as np
from data.data import loadData


def gaussianFunction(x, a, b, c):
    return a * np.exp(-1.0 * np.power(x - b, 2.0) / (2 * c * c))

def gaussianArray(X, a, b, c):
    y = []
    for i in range(0, len(X)):
        y.append(gaussianFunction(X[i], a, b, c))
    return np.array(y)

def func(x, a0, a1, b1, c1, a2, b2, c2, a3, b3, c3):
    y1 = gaussianFunction(x, a1, b1, c1)
    y2 = gaussianFunction(x, a2, b2, c2)
    y3 = gaussianFunction(x, a3, b3, c3)
    return a0 + y1 + y2 + y3

def funcArray(X, a0, a1, b1, c1, a2, b2, c2, a3, b3, c3):
    y = []
    for i in range(0, len(X)):
        y.append(func(X[i], a0, a1, b1, c1, a2, b2, c2, a3, b3, c3))
    return np.array(y)

def fit(X_train, y_train):
    
    a0 = 10.0

    a1 = 30.0
    b1 = 3.0
    c1 = 1.0

    a2 = 80.0
    b2 = 8.0
    c2 = 2.0

    a3 = 60.0
    b3 = 16.0
    c3 = 2.0
    
    p = [a0, a1, b1, c1, a2, b2, c2, a3, b3, c3]
    
    def res(p, y, x):
        a0, a1, b1, c1, a2, b2, c2, a3, b3, c3 = p
        y_fit = funcArray(x, a0, a1, b1, c1, a2, b2, c2, a3, b3, c3)
        err = y - y_fit
        return err
    plsq = leastsq(res, p, args = (y_train, X_train))
    a0 = plsq[0][0]
    a1 = plsq[0][1]
    b1 = plsq[0][2]
    c1 = plsq[0][3]
    a2 = plsq[0][4]
    b2 = plsq[0][5]
    c2 = plsq[0][6]
    a3 = plsq[0][7]
    b3 = plsq[0][8]
    c3 = plsq[0][9]
    return [a0, a1, b1, c1, a2, b2, c2, a3, b3, c3]

# open the airquality preprocessed file
# header: location,timestamp,nox

DATA_FILE = "/media/sf_lur/data/" + "data_hour_2013.csv"
OUTPUT_DIRECTORY = "/media/sf_lur/experiments/ex17/"

data = {}
columns = []
loadData(DATA_FILE, [], data, columns)

stations = {}
#stations[1]="Bootham"
stations[2]="Fulford"
stations[3]="Gillygate"
stations[4]="Heworth"
stations[5]="Holgate"
stations[6]="Lawrence"
stations[7]="Nunnery"
stations[8]="Fishergate"

records = len(data["location"])

# generate statistics

avg = {}
counter = {}

for l in stations:
    avg[l] = {}
    counter[l] = {}
    for i in range(0,24):
        avg[l][i] = 0.0
        counter[l][i] = 0

for i in range(0, records):
    location = int(data["location"][i])
    no2 = data["target"][i]
    key = str(int(data["timestamp"][i]))
    hour = int(key[8:10])
    avg[location][hour] = avg[location][hour] + float(no2)
    counter[location][hour] = counter[location][hour] + 1

for l in stations:
    for i in range(0,24):
        print(str(l))
        print(str(i))
        avg[l][i] = avg[l][i] / float(counter[l][i])

# generate the graph

for l in stations:
    
    print(str(stations[l]))
    
    hours = range(0, 24)
    values = []
    for h in hours:
        values.append(avg[l][h])
    
    a0, a1, b1, c1, a2, b2, c2, a3, b3, c3 = fit(hours, values)
    
    print("a0: " + str(a0))
    print("a1: " + str(a1))
    print("b1: " + str(b1))
    print("c1: " + str(c1))
    print("a2: " + str(a2))
    print("b2: " + str(b2))
    print("c2: " + str(c2))
    print("a3: " + str(a3))
    print("b3: " + str(b3))
    print("c3: " + str(c3))
    
    X_test = []
    for i in range(0,2400):
        X_test.append(float(i)/100.0)

    y_test1 = gaussianArray(X_test, a1, b1, c1)
    y_test2 = gaussianArray(X_test, a2, b2, c2)
    y_test3 = gaussianArray(X_test, a3, b3, c3)

    y_test4 = []
    for i in range(0, len(X_test)):
        y_test4.append(a0)

    y_test5 = funcArray(X_test, a0, a1, b1, c1, a2, b2, c2, a3, b3, c3)
    
    fig = pyplot.figure()
    pyplot.title('Average NO2 levels (' + stations[l] + ')')
    pyplot.ylabel('NO2 (ug/m3)')
    pyplot.xlabel('Hour')
    
    txt0 = "a0: " + str(a0)
    txt1 = "g1: " + str(a1)[:4] + "," + str(b1)[:4] + "," + str(c1)[:4]  
    txt2 = "g2: " + str(a2)[:4] + "," + str(b2)[:4] + "," + str(c2)[:4]  
    txt3 = "g3: " + str(a3)[:4] + "," + str(b3)[:4] + "," + str(c3)[:4]  
    
#     pyplot.text(2, 100, txt0, fontsize=12)
#     pyplot.text(2, 88, txt1, fontsize=12)
#     pyplot.text(2, 76, txt2, fontsize=12)
#     pyplot.text(2, 64, txt3, fontsize=12)
        
    pyplot.xlim(-1, 24)
    pyplot.ylim(-50.0, 150.0)
    
    pyplot.plot(hours, values, marker='o', label='avg')

    pyplot.plot(X_test, y_test1, color='red', label = "g1")
    pyplot.plot(X_test, y_test2, color='green', label = "g2")
    pyplot.plot(X_test, y_test3, color='yellow', label = "g3")
    pyplot.plot(X_test, y_test4, color='orange', label = "a0")
    pyplot.plot(X_test, y_test5, color='grey', label = "prediction")
    
    pyplot.legend(loc='best')    
    
    pyplot.savefig(OUTPUT_DIRECTORY + "graph3_" + stations[l] + ".png")
