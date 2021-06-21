import numpy


class SymmPacker(object):
    """
    Function to Reconstruct Symmetric Matrices from a Compact Form
    The diagonal elements are arranged at the beginning followed by the upper
    triangular elements by row.
    """

    @staticmethod
    def _iu_(n):
        """Constructs arrays representing row and column indices of elements, respectively."""
        temp = numpy.arange(n)
        return tuple(numpy.hstack((temp, x)) for x in numpy.triu_indices(n, 1))

    def __init__(self, n=None):
        self.iu_ = self._iu_(n) if n else None
        self.n_ = n

    def __call__(self, vec, out=None, subs=None):
        n = self.n_
        if n:
            iu = self.iu_
        else:
            n = (int(numpy.sqrt(1 + 8 * vec.size) + 0.5) - 1) // 2
            iu = self._iu_(n)

        if subs is not None:
            assert (all(0 <= x < n for x in subs))
            n = len(subs)
            flag = numpy.logical_and(*(array.logical_in(x, subs) for x in iu))
            vec = vec[flag]
            iu = self._iu_(n)

        if out is None: out = numpy.empty((n, n), dtype=vec.dtype)
        out[iu] = vec
        out[tuple(x[n:] for x in iu[:: -1])] = vec[n:]
        return out
