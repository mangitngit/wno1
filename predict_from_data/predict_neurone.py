import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

data = sio.loadmat('data_map1.mat')
data = data['data_map']

fig = plt.figure()
ax = fig.add_subplot(2, 1, 1, projection='3d')
ax.plot3D(data[:, 0], data[:, 1], data[:, 2])

x1 = np.meshgrid(data[:, 0])
x2 = np.meshgrid(data[:, 1])
f = np.meshgrid(data[:, 2])

x1 = np.transpose(x1)
x2 = np.transpose(x2)
f = np.transpose(f)

X_train = np.hstack((x1, x2))

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)

mlp = MLPRegressor(hidden_layer_sizes=(100, 20))
mlp.fit(X_train, f)

[x11, x22] = np.meshgrid(np.arange(58.82, 59.22, 0.01), np.arange(55.28, 55.68, 0.01))

x11 = x11.flatten()
x22 = x22.flatten()

x11 = np.transpose(x11)
x22 = np.transpose(x22)

x11 = x11.reshape((-1, 1))
x22 = x22.reshape((-1, 1))

X_predict = np.hstack((x11, x22))
X_predict = scaler.transform(X_predict)

Y_predict = mlp.predict(X_predict)

ax = fig.add_subplot(2, 1, 2, projection='3d')
s = ax.plot3D(X_predict[:, 0], X_predict[:, 1], Y_predict)

plt.show()
