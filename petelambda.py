import numpy as np

A = [[-1, 4, -4], [-4, 7, 4], [-4, 4, 1]]

#_lambda = -1, [[1], [1], [1]]
A = np.array(A)
print(A)

# i = np.array([[1], [1], [1]])
i = np.eye(3,3)
i[1,1] = -1
print(i)

_exp = A.T** (1/2)
print(_exp)

_lambda = _exp ** i
print(_lambda)

# verificacion
print( _lambda * A.T)

print(np.sqrt(-(1/2)))

# habia q proyectar el mandelbrot en una curva eliptica y el area de la projeccion era un numero increible
# a una matriz de 3x3.. pero si la matriz es de 4x4?...
