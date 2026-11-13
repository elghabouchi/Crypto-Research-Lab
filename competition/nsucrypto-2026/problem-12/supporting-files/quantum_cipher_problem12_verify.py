"""Problem 12: exact rational verification; Python 3.8+, standard library."""
from fractions import Fraction as F
from itertools import product
from math import log2


def kron(A, B):
    return [[A[i//len(B)][j//len(B[0])] * B[i%len(B)][j%len(B[0])]
             for j in range(len(A[0])*len(B[0]))]
            for i in range(len(A)*len(B))]


def transpose(A): return [list(x) for x in zip(*A)]


def mul(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def scale(c, A): return [[c*a for a in row] for row in A]


def add(A, B): return [[a+b for a, b in zip(r, s)] for r, s in zip(A, B)]


def act(A, v): return [sum(a*b for a, b in zip(row, v)) for row in A]


def dot(a, b): return sum(x*y for x, y in zip(a, b))


def outer(a, b): return [[x*y for y in b] for x in a]


def tensor(a, b): return [x*y for x in a for y in b]


def conjugate(U, A): return mul(mul(U, A), transpose(U))


def average(As):
    As = list(As)
    A = [[0]*len(As[0][0]) for _ in As[0]]
    for B in As: A = add(A, B)
    return scale(F(1, len(As)), A)


def density(v): return scale(F(1, dot(v, v)), outer(v, v))


I = [[1, 0], [0, 1]]
X = [[0, 1], [1, 0]]
R = [[0, -1], [1, 0]]  # Y = i R; global phases do not affect conjugation.
Z = [[1, 0], [0, -1]]
P = [I, X, R, Z]
U = [kron(p, p) for p in P]
U[2] = scale(-1, U[2])  # Actual Y tensor Y, including its Bell phases.
I4, XX, ZZ = kron(I, I), kron(X, X), kron(Z, Z)
BELL = [[1, 0, 0, 1], [1, 0, 0, -1],
        [0, 1, 1, 0], [0, 1, -1, 0]]
# Rows: Phi+, Phi-, Psi+, Psi-; columns: I, X, Y, Z.
PHASES = [[1, 1, -1, 1], [1, -1, 1, 1],
          [1, 1, 1, -1], [1, -1, -1, -1]]
PROJ = [scale(F(1, 2), outer(b, b)) for b in BELL]
for b, phases in zip(BELL, PHASES):
    for gate, s in zip(U, phases): assert act(gate, b) == [s*x for x in b]
print('Bell phase table: all 16 identities verified exactly.')

probe = [1, 1, 0, 0]  # Unnormalized |0+>, squared norm 2.
outputs = [[1, 1, 0, 0], [0, 0, 1, 1],
           [0, 0, 1, -1], [1, -1, 0, 0]]
for k, gate in enumerate(U):
    v = act(gate, probe)
    probs = [F(dot(w, v)**2, dot(w, w)*dot(v, v)) for w in outputs]
    assert probs == [int(i == k) for i in range(4)]
print('Chosen plaintext |0+>: all four key values distinguished with probability 1.')

STATES = {'0': [1, 0], '1': [0, 1], '+': [1, 1], '-': [1, -1]}
BB84 = []
conditional_entropies = []
for a, b in product(STATES, repeat=2):
    v = tensor(STATES[a], STATES[b]); BB84.append(v)
    rho = average(density(act(gate, v)) for gate in U)
    probs = [F(dot(w, v)**2, 2*dot(v, v)) for w in BELL]
    assert sum(probs) == 1
    for gate in U:
        c = act(gate, v)
        assert [F(dot(w, c)**2, 2*dot(c, c)) for w in BELL] == probs
    dephased = [[F(0)]*4 for _ in range(4)]
    for p, Q in zip(probs, PROJ): dephased = add(dephased, scale(p, Q))
    assert rho == dephased
    same_z = a in '01' and b in '01'
    same_x = a in '+-' and b in '+-'
    expected = scale(F(1, 4), I4)
    if same_z or same_x:
        bit_a = int(a in '1-'); bit_b = int(b in '1-')
        corr = ZZ if same_z else XX
        expected = scale(F(1, 4), add(I4, scale((-1)**(bit_a ^ bit_b), corr)))
    assert rho == expected
    for i, j in product(range(2), repeat=2):
        assert sum(rho[2*i+k][2*j+k] for k in range(2)) == F(i == j, 2)
        assert sum(rho[2*k+i][2*k+j] for k in range(2)) == F(i == j, 2)
    conditional_entropies.append(-sum(float(p)*log2(float(p)) for p in probs if p))
print('All 16 allowed plaintext pairs: exact Bell probabilities, averaged states, and marginals verified.')
assert sum(conditional_entropies)/16 == 1.5
assert 2 - sum(conditional_entropies)/16 == 0.5
print('Uniform 16-label ensemble: Bell outcome information = 0.5 bit per pair.')

for gate in U:
    assert average(density(act(gate, v)) for v in BB84) == scale(F(1, 4), I4)
print('Uniform unknown plaintexts: ensemble ciphertext is key-independent, even for a fixed key.')

S = [[int(j == (i%2)*2+i//2) for j in range(4)] for i in range(4)]
for gate in U:
    assert mul(S, gate) == mul(gate, S)
    for p in [X, R, Z]:
        A = kron(p, I)
        C = conjugate(transpose(gate), A)
        assert C == A or C == scale(-1, A)
for v in STATES.values(): assert dot(v, act(R, v)) == 0
print('Malleability: arbitrary local Pauli modification survives decryption; swap commutes with every key.')

proper = [kron(p, q) for p, q in product(P, repeat=2)]
for i, j in product(range(4), repeat=2):
    E = [[int(a == i and b == j) for b in range(4)] for a in range(4)]
    C = average(conjugate(gate, E) for gate in U)
    D = [[F(0)]*4 for _ in range(4)]
    for Q in PROJ: D = add(D, mul(mul(Q, E), Q))
    assert C == D  # Equality of channels on a full operator basis.
    assert average(conjugate(gate, E) for gate in proper) == scale(F(i == j, 4), I4)
restricted = [kron(p, q) for p, q in product([I, R], repeat=2)]
for v in BB84:
    assert average(density(act(gate, v)) for gate in restricted) == scale(F(1, 4), I4)
print('Channel identities: Bell dephasing and independent-Pauli randomization verified on all 16 matrix units.')
print('Restricted-alphabet repair: independent fresh I/Y masks randomize all 16 BB84 product inputs.')
print('PASS: all algebraic assertions use exact integer or rational arithmetic; only entropy uses log2.')
