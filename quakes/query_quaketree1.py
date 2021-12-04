from numpy import zeros, matrix, float64, linalg, arange, array, ndarray
from numpy import array, set_printoptions, inf, nan, savetxt
from pyarma import mat, fill, norm, normalise, log10, stddev, var, mean, median
from pprint import pprint
import sys


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
P1 = normalise(M, p)
print(P1)
set_printoptions(precision=53, threshold=sys.maxsize)
h = ndarray((16, 4))


def quantize(RB):
    W = mean(RB)
    H = stddev(RB)
    OA = var(RB)
    AA = median(RB)
    return W[0], H[0], OA[0], AA[0]


def unroll(M):
    return M.t()


def describe(M, x, y):
    RC = unroll(M)
    C, D, E, F = quantize(RC)
    if C:
        _C = C
    if D:
        _D = D
    if E:
        _E = E
    if F:
        _F = F
    return _C, 0, 0, _F


print(dir(M[:0, 0].t()))
# X = np.allclose([x1.0, np.nan], [1.0, np.nan], equal_nan=True)
for x in arange(M.n_rows):
    for y in arange(M.n_cols):
        s = f"Mat[{x},{y}] = "
        B = M[:x, y]
        C = describe(B, x, y)
        V = s + "mean: %s | stddev: %s | var: %s | median: %s" % C
        print(V)
        f = savetxt(sys.stdout, M)
        # with f as op: attribute error f4 at $s = f"{x} {y}"
