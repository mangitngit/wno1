import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
import copy
# from mpl_toolkits.mplot3d import Axes3D

co_ile_do_obciecia = 20
ile_przewidywania_punkcikow = 1000

data = sio.loadmat('data_map1.mat')
ALL = data["data_map"]
X_column = [i[0] for i in ALL]
Y_column = [i[1] for i in ALL]
Z_column = [i[2] for i in ALL]

Xobcieta = [X_column[i] for i in range(len(X_column)) if i % co_ile_do_obciecia == 0]
Yobcieta = [Y_column[i] for i in range(len(Y_column)) if i % co_ile_do_obciecia == 0]
Zobcieta = [Z_column[i] for i in range(len(Z_column)) if i % co_ile_do_obciecia == 0]

lengene = len(Xobcieta)

Xsort = sorted(Xobcieta)
Ysort = sorted(Yobcieta)

xx, yy = np.meshgrid(Xsort, Ysort)
zz = np.zeros([lengene, lengene])
zz_help = np.zeros([lengene, lengene])

for i in range(lengene):
    for x in range(lengene):
        if Xobcieta[i] == Xsort[x]:
            for y in range(lengene):
                if Yobcieta[i] == Ysort[y]:
                    zz[y][x] = Zobcieta[i]
zz_help = copy.deepcopy(zz)

for no in range(ile_przewidywania_punkcikow):
    for i in range(1, lengene-1):
        for j in range(1, lengene-1):
            zz[i][j] = (zz[i+1][j+1] + zz[i+1][j] + zz[i+1][j-1] + zz[i][j+1] + zz[i][j-1] + zz[i][j] +
                        zz[i-1][j+1] + zz[i-1][j] + zz[i-1][j-1])/9
    for i in range(lengene):
        for j in range(lengene):
            if zz_help[i][j] != 0:
                zz[i][j] = zz_help[i][j]

fig = plt.figure()
ax = fig.add_subplot(2, 1, 1, projection='3d')
ax.plot_surface(xx, yy, zz, cmap=plt.cm.RdBu, linewidth=0, antialiased=False)

ax = fig.add_subplot(2, 1, 2, projection='3d')
ax.plot3D(X_column, Y_column, Z_column)

plt.show()
