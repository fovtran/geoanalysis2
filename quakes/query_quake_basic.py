#!/usr/bin/env python
# pyarma quakeml iterator
from pyarma import mat, fill, norm, normalise, log10
from numpy import zeros, matrix, float64, linalg, arange, array
from sklearn.datasets import make_blobs
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.cluster import MiniBatchKMeans, KMeans
import time
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt


root = readxml()
EV = parsexml(root)

A = zeros((len(EV), 2))
C = zeros((len(EV), 2))
for i, ev in enumerate(EV):
    A[i, 0] = ev['lon']
    A[i, 1] = ev['lat']
    C[i, 0] = ev['val']
    C[i, 1] = ev['depth']

# normalize the norm
M = mat(C)
p = 1
P = linalg.norm(M, p)
_P1 = normalise(M, p)
print(_P1)


# for _x in arange(log.n_rows):
#    for _y in arange(log.n_cols):
#        x.append(log[_x, _P[_x,_y]])
# pip install mpl-scatter-density
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax2 = fig1.add_subplot(1,1,1, projection='3d')
fig = plt.figure(figsize=(15, 7))
ax = fig.add_subplot(1, 2, 1)
ax1 = fig.add_subplot(1, 2, 2)
ax.grid(True)
ax1.grid(True)
R = P/250
surf = ax.scatter(C[::, 0], C[::, 1])
ax.set_xlabel(r'intensidad', fontsize=10)
ax.set_ylabel(r'profundidad', fontsize=10)
surf1 = ax1.scatter(A[::, 0], A[::, 1], s=C[::, 0]
                    * R, c=C[::, 1]/1000, alpha=.8)
ax1.set_xlabel(r'Latitud', fontsize=10)
ax1.set_ylabel(r'Longitud', fontsize=10)
divider = make_axes_locatable(ax1)
cax = divider.new_horizontal(size="1%", pad=-0.5, pack_start=True)
fig.add_axes(cax)
fig.colorbar(surf1, aspect=5, pad=-0.5, cax=cax, orientation="vertical")
plt.show()

# np.allclose([x1.0, np.nan], [1.0, np.nan], equal_nan=True)
