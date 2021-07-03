import numpy as np


def submatrix(n, b, k):
    """
    1) A n*n covariance (symmetric) matrix C is stored in compact vector B by row in that
    [c_{0,0}... c_{n,n}, c_{0,1}... c_{0,n}, c_{1,2}... c_{1,n}, ...].
    Given a separate index vector k that selects a subset of rows and columns of C,
    Write a function to construct a submatrix of C given by k.
    """
    exclude = np.setdiff1d(range(n), k, True)  # exclude irrelevant rows cols
    m = np.zeros((n, n))
    m[exclude, :] = 1
    m[:, exclude] = 1
    mask1 = m[np.diag_indices_from(m)]
    mask2 = m[np.triu_indices_from(m, k=1)]
    mask = np.concatenate((mask1, mask2))
    masked = np.ma.MaskedArray(b, mask, copy=False)
    return np.ma.compressed(masked)


def submatrix2(b, k):
    # (n * n) - ((n - 1) / 2) * (n) = len(b)
    n = int((-1 + np.sqrt(1 + 8 * len(b))) / 2)
    sub = np.zeros((len(k), len(k)))
    sub.ravel()[::n+1][k] = b[k]
    # c[k[:,None],k]
    pass


def overlap(a, k):
    """
    2) Given a m*n array of Fortran layout (col major), create a **view** of (m + k) * n,
    where the first k elements of each column overlaps the last k elements of the previous column. 
    The first few columns may have nonsensical data because of insufficient number of observations.
    """
    offset = np.ndarray(a.shape, dtype=a.dtype, offset=-k * a.strides[0], buffer=a.data, order='F')
    return np.lib.stride_tricks.as_strided(offset, shape=((a.shape[0] + k), a.shape[1]), strides=offset.strides)


print('1)', submatrix(3, [1, 5, 9, 2, 3, 6], [1, 2]))
print('2) a.')
b = np.asarray([[1,  2,  3,  4], [5,  6,  7,  8], [9, 10, 11, 12]], order='F')
print(b)
print(overlap(b, 2))
print('2) b.')
c = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], order='F')
print(c)
print(overlap(c, 3))
