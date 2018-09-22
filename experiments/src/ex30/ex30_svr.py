from ex30.ex30_lib_graph import plot2
from sklearn.svm.classes import SVR

OUTPUT_PNG_FILE = '/experiments/ex30/ex30_svr.png'

X = [[float(x)] for x in range(0,24)]
Y = [12.0, 13.0, 13.0, 13.0, 28.0, 31.0, 38.0, 60.0, 85.0, 80.0, 64.0, 60.0, 59.0, 58.0, 65.0, 70.0, 80.0, 90.0, 110.0, 100.0, 85.0, 65.0, 45.0, 20.0 ]

X2 = [[float(x)/10.0] for x in range(0,231)]

model = SVR(kernel='rbf', C=10)
model.fit(X, Y)
Y_pred = model.predict(X2)

print(str(Y_pred))

plot2(
    Y, 
    Y_pred, 
    OUTPUT_PNG_FILE,
    "Observed pollution concentration levels",
    "Predicted pollution concentration levels by SVR")

