def gsp(basis):
    if len(basis) == 1:
        return basis
    else:
        obasis = gsp(basis[:-1])
        obasis.append(orthog(obasis, basis[-1]))
        return obasis


def orthog(obasis, y):
    """Returns the orthogonal component of y with respect to orthogonal obasis."""
    proj = []  # list of projections of y onto each vector of obasis.
    for u in obasis:
        v = []  # proj_u(y)
        c = dot(u, y) / dot(u, u)
        for x in u:  # element of basis vector
            v.append(c * x)
        proj.append(v)
    for p in proj:
        y = sub(y, p)
    return y


def sub(y, p):
    v = []
    for i in range(len(y)):
        v.append(y[i] - p[i])
    return v


def dot(u, v):
    """Returns the dot product of two vectors of the same dimension."""
    prod = 0
    for i in range(len(u)):
        prod += u[i] * v[i]
    return prod


if __name__ == "__main__":
    # inp = input("Input a list of vectors in the same dimension, ex. [[1,0],[0,1]]")
    # convert to list of tuples
    b = [[1, 1, 1], [1, 2, 0], [2, 0, 1]]
    print(gsp(b))
