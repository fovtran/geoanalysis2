import sys
import matplotlib.pyplot as plt
from pprint import pprint
from pyarma import mat, fill, norm, normalise
from pyarma import log, log10, stddev, var, mean, median, conj
from numpy import zeros, matrix, float64, linalg, arange, array, ndarray, array
from numpy import set_printoptions, inf, nan, savetxt, savez, load
set_printoptions(precision=14, threshold=sys.maxsize)

debug = False


def quantize(RB):
    """Get the values of mean, std"""
    W = mean(RB)
    H = stddev(RB, norm_type=1)
    OA = var(RB, norm_type=1)
    AA = median(RB)
    return W[0], H[0], OA[0], AA[0]


def unroll(M):
    return M.t()


def describe(X, M):
    """Returns the mean and std values for a rowcolumn matrix"""
    x, y = X[0], X[1]
    B = M[:x, y]
    RC = unroll(M)
    W, _std, _var, F = quantize(RC)
    if W:
        _W = W
    if F:
        _F = F
    return _W, _std, _var, _F


def map_closeness(M):
    """Computes and returns model description"""
    _total_mean = 0
    U = mat(M.n_rows, 1, fill.zeros)
    for x in arange(M.n_rows):
        for y in arange(M.n_cols):
            s = f"Mat[{x},{y}] = "
            coord = (x, y)
            C = describe(coord, M)
            U[x] = C[0]
            V = s + "mean: %s | stddev: %s | var: %s | median: %s" % C
            print(V)
            f = savetxt(sys.stdout, M)
            """ # with f as op: attribute error f4 at $s = f"{x} {y}" """
            # return V
        yield U
    # return U


def QuakeMap():
    """Returns a two tables of spatial and weighted data"""
    filename = 'boxtree.xml'
    Q = quakeml(filename)
    Q.parse_quakeml()
    for ev in Q.get_data():
        EXA = ev
        A = zeros((len(EXA), 2))
        C = zeros((len(EXA), 2))
        for i, event in enumerate(EXA):
            A[i, 0] = event['lon']
            A[i, 1] = event['lat']
            C[i, 0] = event['val']
            C[i, 1] = event['depth']
    return A, C


# Get the datasets in armadillo matrix format
A, C = QuakeMap()
U = mat(A)
V = mat(C)

pfilename = 'my-pickle'
savez('my-pickle', A=A, C=C, U=U, V=V)
db = load(pfilename+".npz")


M = V

if debug:
    print(M[:0, 0].t())
# routine used to
# reduce map X = np.allclose([x1.0, np.nan], [1.0, np.nan], equal_nan=True)

_std = map_closeness(M)
print("---")
prev = 1
X = []
for i, STD in enumerate(_std):
    current = STD
    X.append(mean(current))
    prev = current
    S = ("mean: %s" % array(X[i])[0])
    # f = savetxt(sys.stdout, S)
    # print(f"res={X[i][0]}")
    print(f"mean={S}")

p = 1
P = linalg.norm(U, p)
_norm = normalise(M, p)
print("norm:")
f = savetxt(sys.stdout, _norm)

_conj = conj(M)
_conj.print("conjugate:")

_log = log(_conj)
_logn = log10(_conj)
_log.print("log10:")

# h = ndarray((16, 4))
X2 = array(_logn)[:, 0]
X3 = array(_conj)[:, 0]
X4 = array(_conj)[:, 1]

fig = plt.figure(figsize=(14, 7))

ax1 = fig.add_subplot(3, 1, 1)
ax1.set_title("Depth Increment vs event_id()")
ax1.grid(True)
ax1.hist2d(arange(len(X2)), X2)   # , color='violet')

ax2 = fig.add_subplot(3, 1, 2)
surf = ax2.scatter(
    1-array(_logn[::, 0]),
    -X4/1000,
    s=1+V[::, 0]*100,
    c=1+V[::, 1],
    alpha=.7
    )
ax2.set_title("Earthquake Strength vs Probability Depth")
ax2.grid(True)
fig.colorbar(surf, aspect=5, pad=0.2, orientation="vertical")


ax3 = fig.add_subplot(3, 1, 3)
ax3.set_title("Earthquake Strength vs ProbabilityIncrement")
ax3.scatter(C[::, 1], X4*-P, color='orange')

plt.tight_layout(pad=1)
# plt.subplots_adjust(top=1, bottom=-1)
plt.show()
# !done
