import numpy


class SymmPacker(object):
    """
    Function to Reconstruct Symmetric Matrices from a Compact Form
    The diagonal elements are arranged at the beginning followed by the upper
    triangular elements by row.
    """

    @staticmethod
    def _iu_(n):
        """Constructs arrays representing row and column indices of elements in upper triangle"""
        temp = numpy.arange(n)
        return tuple(numpy.hstack((temp, x)) for x in numpy.triu_indices(n, 1))

    def __init__(self, n=None):
        self.iu_ = self._iu_(n) if n else None
        self.n_ = n

    def __call__(self, vec, out=None, subs=None):
        # init if not already
        n = self.n_
        if n:
            iu = self.iu_
        else:
            n = (int(numpy.sqrt(1 + 8 * vec.size) + 0.5) - 1) // 2
            iu = self._iu_(n)

        if subs is not None:
            assert (all(0 <= x < n for x in subs))
            n = len(subs)  # dims of new array
            print(iu)
            print(subs)
            flag = numpy.logical_and(*(logical_in(x, subs) for x in iu))  # indices that are selected
            vec = vec[flag]
            iu = self._iu_(n)  # upper indicies of new arr

        if out is None: out = numpy.empty((n, n), dtype=vec.dtype)
        out[iu] = vec
        out[tuple(x[n:] for x in iu[:: -1])] = vec[n:]
        return out


def logical_in(x, sub):
    """returns indices, passed as x, which are in sub"""
    return [True if y in sub else False for y in x]


test = SymmPacker(3)
print(test([1, 5, 9, 2, 3, 6], subs=[1, 2]))

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
