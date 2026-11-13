"""Problem 9: exhaustive verification of explicitly listed finite cases.
The general assertion is not proved by this program. Python 3.8+.
"""
from itertools import combinations
from math import gcd, prod
from time import perf_counter

def field(N, f):
    q = 1 << N
    exp, log = [1], [-1] * q
    for _ in range(q - 2):
        x = exp[-1] << 1
        if x & q: x ^= f
        assert x != 1
        exp.append(x)
    x = exp[-1] << 1
    if x & q: x ^= f
    assert x == 1 and len(set(exp)) == q - 1
    for i, x in enumerate(exp): log[x] = i
    def mul(a, b):
        return 0 if not a or not b else exp[(log[a] + log[b]) % (q-1)]
    return mul, log, exp

def spaces(N, n):
    # Unique reduced bases, with lowest set bits as pivots.
    for piv in combinations(range(1, N), n-1):
        free = [(i, j) for i, p in enumerate(piv)
                for j in range(p+1, N) if j not in piv]
        for mask in range(1 << len(free)):
            b = [1] + [1 << p for p in piv]
            for k, (i, j) in enumerate(free):
                if mask >> k & 1: b[i+1] ^= 1 << j
            yield b

def rank(xs, N):
    basis = [0] * N
    for a in xs:
        while a:
            k = a.bit_length()-1
            if basis[k]: a ^= basis[k]
            else:
                basis[k] = a
                break
    return sum(x != 0 for x in basis)

def run(N, n, f):
    m, tau = N // n, (1 << N)-1
    mul, log, exp = field(N, f)
    ds = [d for d in range(1, tau) if gcd(d, tau) == 1]
    cache = []
    def powers(j):
        if j == len(cache):
            d = ds[len(cache)]; beta = exp[d]; p = [1]
            for _ in range(m-1): p.append(mul(p[-1], beta))
            cache.append((d, p))
        return cache[j][1]
    total = survivors = 0
    survivor = None
    started = perf_counter()
    for b in spaces(N, n):
        total += 1
        # The proved subfield construction passes every primitive beta.
        if all(log[x] * ((1 << n)-1) % tau == 0 for x in b):
            survivors += 1; survivor = b
            continue
        for j in range(len(ds)):
            p = powers(j)
            if rank([mul(x, y) for y in p for x in b], N) != N:
                break
        else: raise AssertionError('Non-subfield survivor: ' + repr(b))
    expected = prod(2**(N-1-i)-1 for i in range(n-1))
    expected //= prod(2**(n-1-i)-1 for i in range(n-1))
    assert total == expected and survivors == 1
    print(f'N={N:2} n={n} m={m:2} f={f:x} spaces={total} '
          f'survivors={survivors} max_tests={len(cache)} '
          f'ds={[d for d,_ in cache]} basis={survivor} '
          f'seconds={perf_counter()-started:.3f}', flush=True)

CASES = [(4,2,0x13), (6,2,0x43), (6,3,0x43),
         (8,2,0x11d), (8,4,0x11d), (9,3,0x211),
         (10,2,0x409), (10,5,0x409),
         (12,2,0x1053), (12,3,0x1053),
         (14,2,0x4443), (16,2,0x1100b),
         (18,2,0x40081), (20,2,0x100009)]
if __name__ == '__main__':
    for case in CASES: run(*case)
