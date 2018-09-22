from ex30.ex30_lib_graph import plot2
from sknn.mlp import Regressor, Layer
import numpy as np
from sklearn.preprocessing.data import StandardScaler

OUTPUT_PNG_FILE = '/experiments/ex30/ex30_ann.png'

X = [[float(x), float(x), float(x)] for x in range(0,24)]
Y = [12.0, 13.0, 13.0, 13.0, 28.0, 31.0, 38.0, 60.0, 85.0, 80.0, 64.0, 60.0, 59.0, 58.0, 65.0, 70.0, 80.0, 90.0, 110.0, 100.0, 85.0, 65.0, 45.0, 20.0 ]

X2 = [[float(x)/10.0, float(x)/10.0, float(x)/10.0] for x in range(0,231)]
    
layers = []
layers.append(Layer("Rectifier", units=100))
layers.append(Layer("Rectifier", units=100))
layers.append(Layer("Rectifier", units=100))
layers.append(Layer("Linear"))

model = Regressor(
    layers=layers,
    learning_rate=0.001,
    n_iter=5000,
    random_state=42)

normalizer_X = StandardScaler()
trainX = normalizer_X.fit_transform(X)
trainX2 = normalizer_X.fit_transform(X2)
normalizer_Y = StandardScaler()
trainY = normalizer_Y.fit_transform(Y)

model.fit(np.array(trainX), np.array(trainY))
Y_pred = model.predict(np.array(trainX2))
Y_pred = normalizer_Y.inverse_transform(Y_pred)

Y_pred = [y[0] for y in Y_pred]

print(str(Y_pred))

plot2(
    Y, 
    Y_pred, 
    OUTPUT_PNG_FILE,
    "Observed pollution concentration levels",
    "Predicted pollution concentration levels by ANR")

