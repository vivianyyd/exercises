import math


def sub(y, p):
    """Returns the difference of two vectors of the same dimension."""
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


def proj(obasis, y):
    """Returns the projection of y onto the vector space spanned by vectors in orthogonal obasis."""
    pr = []  # list of projections of y onto each vector of obasis.
    for u in obasis:
        v = []  # proj_u(y)
        c = dot(u, y) / dot(u, u)
        for x in u:  # element of basis vector
            v.append(c * x)
        pr.append(v)
    return pr


def orthog(obasis, y):
    """Returns the orthogonal component of y with respect to orthogonal obasis."""
    for p in proj(obasis, y):
        y = sub(y, p)
    return y


def gsp(basis):
    """Returns an orthogonal basis for the vector space spanned by basis."""
    if len(basis) == 1:
        return basis
    else:
        obasis = gsp(basis[:-1])
        obasis.append(orthog(obasis, basis[-1]))
        return obasis


def least_squares_proj(basis, y):
    """Returns the least-squares solution x (closest approximation) to the system Ax=y,
    where A is the matrix with columns in basis, by projecting y onto Span{basis}."""
    obasis = gsp(basis)
    return proj(obasis, y)


def least_squares_qr():
    pass


def all_but(a, i):
    """
    Returns the matrix formed by removing row 0 and column i of a.
    """
    res = []
    for row in a[1:]:
        res.append(row[:i] + row[i + 1:])
    return res
    pass


def det_cofactor(a):
    """Recursively computes the determinant of a matrix using cofactor expansion."""
    cof = 0
    for i in range(a[0]):
        cof += math.pow(-1, i) * a[0][i] * det_cofactor(all_but(a, i))
    return cof


def pretty(matrix):
    """Pretty prints matrix, given input as a list of columns in the matrix."""
    if not hasattr(matrix[0], '__iter__'):
        print(matrix)
    elif len(matrix) == 0 or len(matrix[0]) == 0:
        print('empty matrix')
    else:
        col_widths = [0 for j in range(len(matrix))]
        for j in range(len(matrix)):
            for elem in matrix[j]:
                col_widths[j] = len(str(elem)) if len(str(elem)) > col_widths[j] else col_widths[j]
        for i in range(len(matrix[0])):
            row = '['
            for j in range(len(matrix) - 1):
                elem = str(matrix[j][i])
                row += elem + (' ' * (col_widths[j] - len(elem) + 1))
            elem = str(matrix[len(matrix) - 1][i])
            row += elem + (' ' * (col_widths[len(matrix) - 1] - len(elem))) + ']'
            print(row)


if __name__ == "__main__":
    m = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    pretty(m)
    print('All but 0th row, 1st column:')
    pretty(all_but(m, 1))

    # inp = input("Input a list of vectors in the same dimension, ex. [[1,0],[0,1]]")
    # convert to list of tuples

    b = [[1, 1, 1], [1, 12345, 0], [2, 0, 1]]
    print('Orthogonal basis for')
    pretty(b)
    pretty(gsp(b))
