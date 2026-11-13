"""Exact solution of NSUCRYPTO 2026, Problem 4: Secret coding.
Python 3.10+; standard library only. Run without Python's -O option.
All 3^6 error prefixes are tested; no integrality of s is assumed.
"""
from fractions import Fraction
from itertools import product
from math import lcm

A = [
    [-5, -8, 0, -1, -1, -4],
    [-5, -6, 5, -7, -8, -6],
    [-2, -1, 8, -8, -2, 5],
    [-1, 6, 0, -8, -3, 5],
    [2, 0, -4, -2, 2, -5],
    [-6, 4, -5, 3, 3, 0],
    [34, -8, -9, 12, 12, -8],
    [30, -8, -1, 16, 39, 2],
    [9, 5, 29, -11, -9, -7],
    [-37, -3, -58, 12, -4, 32],
    [4, -30, -12, 6, 35, -10],
    [-30, 22, -56, 0, -42, 25],
]
b = [-18, -1, 83, 37, -8, -85, 156, 231, 142, -340, 96, -426]


def dot(u, v):
    return sum(x*y for x, y in zip(u, v))


def solve_square(matrix, rhs):
    """Gauss-Jordan elimination over exact rational numbers."""
    n = len(matrix)
    mat = [[Fraction(x) for x in row] + [Fraction(y)]
           for row, y in zip(matrix, rhs)]
    determinant = Fraction(1)
    for k in range(n):
        pivot = next(i for i in range(k, n) if mat[i][k])
        if pivot != k:
            mat[k], mat[pivot] = mat[pivot], mat[k]
            determinant = -determinant
        value = mat[k][k]
        determinant *= value
        mat[k] = [x/value for x in mat[k]]
        for i in range(n):
            if i != k:
                value = mat[i][k]
                mat[i] = [x-value*y for x, y in zip(mat[i], mat[k])]
    return [row[-1] for row in mat], determinant


B = A[:6]
BT = [list(col) for col in zip(*B)]
weights, determinant = solve_square(BT, A[6])
assert determinant == 225040
D = lcm(*(x.denominator for x in weights))
w = [int(D*x) for x in weights]
assert D == 45008
assert w == [22130, -85711, -51212, -22471, 83479, -153419]
assert all(sum(w[i]*A[i][j] for i in range(6)) == D*A[6][j]
           for j in range(6))
syndrome = D*b[6] - dot(w, b[:6])
assert syndrome == 43117

# Every admissible solution must pass this integer identity.
errors = list(product((-1, 0, 1), repeat=6))
matches = {}
for e7 in (-1, 0, 1):
    target = D*e7 - syndrome
    matches[e7] = [u for u in errors if dot(w, u) == target]
    print('e7 =', e7, 'target =', target, 'matches =', matches[e7])
assert matches == {-1: [], 0: [], 1: [(1, -1, 0, 1, -1, 0)]}
u = matches[1][0]
s, determinant = solve_square(B, [b[i]-u[i] for i in range(6)])
e = [Fraction(bi)-dot(row, s) for row, bi in zip(A, b)]
assert s == [7, -4, 3, -6, 2, 5]
assert e == [1, -1, 0, 1, -1, 0, 1, 0, -1, 1, 0, -1]
assert all(abs(x) <= 10 for x in s)
assert all(x in (-1, 0, 1) for x in e)
assert all(dot(row, s)+ei == bi for row, ei, bi in zip(A, e, b))

# Check the compact 27-by-27 uniqueness certificate.
L = {dot(w[:3], u) for u in product((-1, 0, 1), repeat=3)}
R = {dot(w[3:], u) for u in product((-1, 0, 1), repeat=3)}
assert len(L) == len(R) == 27
for e7 in (-1, 0, 1):
    target = D*e7 - syndrome
    common = L & {target-r for r in R}
    assert common == ({107841} if e7 == 1 else set())
    print('e7 =', e7, 'intersection =', sorted(common))
print('s =', tuple(int(x) for x in s))
print('e =', tuple(int(x) for x in e))
print('i, b_i, a_i*s, e_i')
for i, (row, bi, ei) in enumerate(zip(A, b, e), 1):
    print(i, bi, int(dot(row, s)), int(ei))
print('ALL EXACT CHECKS PASSED; THE SOLUTION IS UNIQUE.')
