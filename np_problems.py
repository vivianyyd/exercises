import numpy as np


def submatrix(n, b, k):  # TODO: questions - used b instead of c lol, should i calculate n, what form returned
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
    print(mask)
    masked = np.ma.MaskedArray(b, mask, copy=False)
    print(masked)
    return np.ma.compressed(masked)


def submatrix2(b, k):
    """
    A n*n covariance (symmetric) matrix C is stored in compact vector B by row in that
    [c_{0,0}... c_{n,n}, c_{0,1}... c_{0,n}, c_{1,2}... c_{1,n}, ...].
    Given a separate index vector k that selects a subset of rows and columns of C,
    Write a function to construct a submatrix of C given by k.
    """
    # (n * n) - ((n - 1) / 2) * (n) = len(b)
    n = int((-1 + np.sqrt(1 + 8 * len(b))) / 2)
    sub = np.zeros((len(k), len(k)))
    sub.ravel()[::n+1][k] = b[k]

    # c[k[:,None],k]

    '''
    take
    place
    putmask
    put
    '''
    pass


''' c
1 2 3
2 5 6
3 6 9

sub
5 6
6 9
'''
# print(submatrix(3, [1, 5, 9, 2, 3, 6], [1, 2]))

'''
00 01 02 03 04
10 11 12 13 14
20 21 22 23 24
30 31 32 33 34
40 41 42 43 44
'''


def overlap(a, k):
    """
    Given a m*n array of Fortran layout (col major), create a **view** of (m + k) * n, 
    where the first k elements of each column overlaps the last k elements of the previous column. 
    The first few columns may have nonsensical data because of insufficient number of observations.
    k = 2
    1  2  3  4      x  5  6  7
    5  6  7  8      x  9 10 11
    9 10 11 12      1  2  3  4
                    5  6  7  8
                    9 10 11 12
    each column starts from
    """
    # TODO fix
    offset = np.ndarray(a.shape, dtype=a.dtype, offset=-2 * k * a.shape[0], buffer=a.data, order='F')
    print(offset)
    return np.lib.stride_tricks.as_strided(offset, shape=((a.shape[0] + k), a.shape[1]), strides=offset.strides, writeable=False)


# nonworking example with function call
b = np.asarray([[1,  2,  3,  4], [5,  6,  7,  8], [9, 10, 11, 12]], order='F')
print(b)
print(overlap(b, 2))

# working example
c = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], order='F')
print(c)
j = 2
w = np.ndarray(c.shape, dtype=c.dtype, offset=-2 * j * c.shape[0], buffer=c.data, order='F')
x = np.lib.stride_tricks.as_strided(w, shape=((c.shape[0] + j), c.shape[1]), strides=w.strides, writeable=False)
print(x)
# TODO as_strided source
