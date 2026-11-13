"""Exact m=2 verifier for Vector LRS (Python 3.10+ standard library only).

Usage:
  python vector_lrs_m2_verify.py --original      # fourteen original cases
  python vector_lrs_m2_verify.py --near-subfield # finite certificates
  python vector_lrs_m2_verify.py                 # n=2,...,10
  python vector_lrs_m2_verify.py --n 6 7 8 9
  python vector_lrs_m2_verify.py --validate      # independent small cases

The search enumerates reduced-basis prefixes; it is exhaustive with exact pruning.
The proof of pruning/completeness is in Vector_LRS_Final.tex, Section 6.
It does not prove the unrestricted classification.
"""
import sys
if not __debug__:
    raise RuntimeError('Run without -O: certificate checks use assertions.')
from math import gcd

def field(N, f):
    assert N >= 2 and f.bit_length() == N + 1 and (f & 1 == 1)
    Q = 1 << N
    M = Q - 1
    exp = [1]
    log = [-1] * Q
    for i in range(M - 1):
        x = exp[-1] << 1
        if x & Q:
            x ^= f
        assert x != 1
        exp.append(x)
    assert exp[-1] << 1 ^ (f if exp[-1] & Q >> 1 else 0) == 1
    assert len(set(exp)) == M
    for i, x in enumerate(exp):
        log[x] = i

    def mul(a, b):
        return 0 if not a or not b else exp[(log[a] + log[b]) % M]

    def inv(a):
        assert a != 0
        return exp[-log[a] % M]
    return (exp, log, mul, inv)

def orbit(t, inv):
    return {t, t ^ 1, inv(t), inv(t) ^ 1, inv(t ^ 1), inv(t ^ 1) ^ 1}
from time import perf_counter
from pathlib import Path
import json

def run_bitsets(n, f):
    N = 2 * n
    Q = 1 << N
    M = Q - 1
    exp, log, mul, inv = field(N, f)
    prim = {exp[i] for i in range(1, M) if gcd(i, M) == 1}
    bad = set().union(*(orbit(x, inv) for x in prim))
    B = [x for x in range(Q) if x not in bad]
    adj = {}

    def neighbors(w):
        if w not in adj:
            buf = bytearray(Q // 8)
            for b in B:
                z = mul(w, b)
                buf[z >> 3] |= 1 << (z & 7)
            adj[w] = int.from_bytes(buf, 'little')
        return adj[w]
    levels = [0] * (n + 1)
    survivors = []
    start = perf_counter()

    def rec(basis, U, C, piv):
        d = len(basis)
        levels[d] += 1
        if N <= 8:
            assert all((mul(a, inv(b)) not in prim for a in U if a for b in U if b))
        if d == n:
            survivors.append(basis)
            return
        low = 1 << basis[-1].bit_length()
        opts = C >> low << low
        maxp = N - (n - d)
        opts &= (1 << (1 << maxp + 1)) - 1
        while opts:
            bit = opts & -opts
            opts ^= bit
            x = bit.bit_length() - 1
            if x & piv:
                continue
            coset = [x ^ u for u in U]
            if any((not C >> z & 1 for z in coset)):
                continue
            nxt = C
            for z in coset:
                nxt &= neighbors(z)
            rec(basis + [x], U + coset, nxt, piv | 1 << x.bit_length() - 1)
    rec([1], [0, 1], neighbors(1), 1)
    S = {0} | {exp[i * M // ((1 << n) - 1)] for i in range((1 << n) - 1)}
    for b in survivors:
        U = [0]
        for x in b:
            U += [u ^ x for u in U]
        assert set(U) == S, ('COUNTEREXAMPLE', n, b)
    assert len(survivors) == 1, ('Unexpected survivor count', n, survivors)
    ans = {'n': n, 'm': 2, 'modulus': hex(f), 'levels': levels, 'survivors': survivors, 'allowed_count': len(B), 'cached_neighbors': len(adj), 'seconds': perf_counter() - start}
    print(json.dumps(ans), flush=True)
    return ans
from itertools import combinations
from cmath import exp as cexp
from math import pi, sqrt, prod, isqrt
import argparse

def validate():

    def spaces(N, n):
        for piv in combinations(range(1, N), n - 1):
            free = [(i, j) for i, p in enumerate(piv) for j in range(1, p) if j not in piv]
            for mask in range(1 << len(free)):
                b = [1] + [1 << p for p in piv]
                for k, (i, j) in enumerate(free):
                    if mask >> k & 1:
                        b[i + 1] ^= 1 << j
                yield b

    def span(b):
        U = [0]
        for x in b:
            U += [u ^ x for u in U]
        return U

    def rank(xs):
        bs = {}
        for x in xs:
            while x:
                j = x.bit_length() - 1
                if j in bs:
                    x ^= bs[j]
                else:
                    bs[j] = x
                    break
        return len(bs)
    ans = {}
    for n, f in [(2, 19), (3, 67), (4, 285)]:
        N = 2 * n
        ex, lg, mu, iv = field(N, f)
        M = (1 << N) - 1
        prim = [ex[j] for j in range(1, M) if gcd(j, M) == 1]
        bad = set().union(*(orbit(x, iv) for x in prim))
        count = 0
        raw = []
        for b in spaces(N, n):
            count += 1
            U = span(b)
            ratio_ok = all((mu(a, iv(v)) not in bad for a in U[1:] for v in U[1:]))
            rank_ok = all((rank(b + [mu(p, x) for x in b]) == N for p in prim))
            assert ratio_ok == rank_ok
            if rank_ok:
                raw.append(b)
        fast = run(n, f)
        assert raw == fast['survivors']
        ans[str(n)] = {'spaces': count, 'survivors': raw}
        print('independent complete comparison', n, count, len(raw), flush=True)
    for s, f in [(2, 19), (3, 67)]:
        N = 2 * s
        q = 1 << s
        ex, lg, mu, iv = field(N, f)
        M = q * q - 1
        S = [0] + [ex[j * (q + 1)] for j in range(q - 1)]

        def tr(x):
            z = 0
            for _ in range(s):
                z ^= x
                x = mu(x, x)
            assert z in [0, 1]
            return z
        signs = [[1 - 2 * tr(mu(a, x)) for x in S] for a in S]
        maxmix = 0
        maxplain = 0
        tests = 0
        for t in range(1 << N):
            if t in S:
                continue
            for j in range(1, M):
                vals = [cexp(2j * pi * (j * lg[t ^ x] % M) / M) for x in S]
                pure = abs(sum(vals))
                assert pure <= sqrt(q) + 1e-08
                maxplain = max(maxplain, pure)
                for sig in signs:
                    v = abs(sum((z * e for z, e in zip(vals, sig))))
                    assert v <= 2 * sqrt(q) + 1e-08
                    maxmix = max(maxmix, v)
                    tests += 1
        print('mixed sums', q, tests, maxplain, maxmix, flush=True)
        ans['mixed_' + str(q)] = {'tests': tests, 'max_pure': maxplain, 'max_mixed': maxmix}
    return ans
BRIDGE_FACTORS = {19: [3, 174763, 524287], 20: [3, 5, 5, 11, 17, 31, 41, 61681], 21: [3, 3, 7, 7, 43, 127, 337, 5419], 22: [3, 5, 23, 89, 397, 683, 2113], 23: [3, 47, 178481, 2796203], 24: [3, 3, 5, 7, 13, 17, 97, 241, 257, 673], 25: [3, 11, 31, 251, 601, 1801, 4051], 26: [3, 5, 53, 157, 1613, 2731, 8191], 27: [3, 3, 3, 3, 7, 19, 73, 87211, 262657], 28: [3, 5, 17, 29, 43, 113, 127, 15790321], 29: [3, 59, 233, 1103, 2089, 3033169], 30: [3, 3, 5, 5, 7, 11, 13, 31, 41, 61, 151, 331, 1321], 31: [3, 715827883, 2147483647], 32: [3, 5, 17, 257, 641, 65537, 6700417], 33: [3, 3, 7, 23, 67, 89, 683, 20857, 599479], 34: [3, 5, 137, 953, 26317, 43691, 131071], 35: [3, 11, 31, 43, 71, 127, 281, 86171, 122921], 36: [3, 3, 3, 5, 7, 13, 17, 19, 37, 73, 109, 241, 433, 38737], 37: [3, 223, 1777, 25781083, 616318177], 38: [3, 5, 229, 457, 174763, 524287, 525313]}

def verify_geometric_family_bridge():

    def prime_trial(p):
        if p < 2:
            return False
        if p % 2 == 0:
            return p == 2
        return all((p % d for d in range(3, isqrt(p) + 1, 2)))
    data = BRIDGE_FACTORS
    out = []
    for n, fs in data.items():
        assert prod(fs) == (1 << 2 * n) - 1
        assert all((prime_trial(p) for p in fs))
        w = len(set(fs))
        assert 1 << n - 4 > ((1 << w) - 1) ** 2
        out.append({'n': n, 'omega': w, 'prime_factors_with_multiplicity': fs})
    ps = [p for p in range(3, 64, 2) if prime_trial(p)]
    assert len(ps) == 17 and prod(ps) > 2 ** 75
    return out

def run_set(n, f):
    N = 2 * n
    Q = 1 << N
    M = Q - 1
    ex, lg, mul, iv = field(N, f)
    prim = {ex[j] for j in range(1, M) if gcd(j, M) == 1}
    bad = set().union(*(orbit(x, iv) for x in prim))
    A = set(range(Q)) - bad
    goodlog = bytearray([1]) * M
    for x in bad:
        goodlog[lg[x]] = 0
    levels = [0] * (n + 1)
    survivors = []
    start = perf_counter()

    def rec(basis, U, C, piv):
        d = len(basis)
        levels[d] += 1
        if d == n:
            survivors.append(basis)
            return
        low = 1 << basis[-1].bit_length()
        high = 1 << N - (n - d) + 1
        for x in sorted((a for a in C if low <= a < high and (not a & piv))):
            coset = [x ^ u for u in U]
            if any((z not in C for z in coset)):
                continue
            if d + 1 == n:
                rec(basis + [x], U + coset, set(), piv | 1 << x.bit_length() - 1)
                continue
            nxt = C
            for z in coset:
                lz = lg[z]
                nxt = {a for a in nxt if a == 0 or goodlog[(lg[a] - lz) % M]}
                if len(nxt) < 1 << n:
                    break
            else:
                rec(basis + [x], U + coset, nxt, piv | 1 << x.bit_length() - 1)
    rec([1], [0, 1], A, 1)
    S = {0} | {ex[i * M // ((1 << n) - 1)] for i in range((1 << n) - 1)}
    assert len(survivors) == 1
    for b in survivors:
        U = [0]
        for x in b:
            U += [u ^ x for u in U]
        assert set(U) == S
    ans = {'n': n, 'm': 2, 'modulus': hex(f), 'levels': levels, 'survivors': survivors, 'allowed_count': len(A), 'engine': 'sets_with_completion_cardinality_pruning', 'seconds': perf_counter() - start}
    print(json.dumps(ans), flush=True)
    return ans
run = run_set

def verify_near_subfields(cases, independent=False):

    def prime_trial(p):
        if p < 2:
            return False
        if p % 2 == 0:
            return p == 2
        return all((p % d for d in range(3, isqrt(p) + 1, 2)))

    def binary_rank(xs):
        basis = {}
        for x in xs:
            while x:
                j = x.bit_length() - 1
                if j in basis:
                    x ^= basis[j]
                else:
                    basis[j] = x
                    break
        return len(basis)
    summaries = []
    for cert in cases:
        n = cert['n']
        q = 1 << n
        M = q * q - 1
        f = int(cert['modulus'], 16)
        ex, lg, mul, iv = field(n, f)

        def tr(a):
            t = 0
            for _ in range(n):
                t ^= a
                a = mul(a, a)
            assert t in (0, 1)
            return t
        delta = cert['delta']
        assert tr(delta) == 1

        def kmul(x, y):
            a, b = x
            c, d = y
            bd = mul(b, d)
            return (mul(a, c) ^ mul(bd, delta), mul(a, d) ^ mul(b, c) ^ bd)

        def power(x, e):
            y = (1, 0)
            while e:
                if e & 1:
                    y = kmul(y, x)
                x = kmul(x, x)
                e >>= 1
            return y
        fs = cert['prime_factors']
        assert all((prime_trial(p) for p in fs))
        unfactored = M
        for p in fs:
            assert unfactored % p == 0
            while unfactored % p == 0:
                unfactored //= p
        assert unfactored == 1

        def mask(c):
            return sum((tr(mul(c, 1 << i)) << i for i in range(n)))
        candidates = [(b, h) for b in range(1, q) for h in (0, 1)]
        if independent and n <= 4:
            wb = []
            for w in range(1, q):
                if tr(w) == 0 and binary_rank(wb + [w]) > len(wb):
                    wb.append(w)
            assert len(wb) == n - 1
        for step in cert['checks']:
            r, z = step['beta']
            assert z != 0
            assert power((r, z), M) == (1, 0)
            assert all((power((r, z), M // p) != (1, 0) for p in fs))
            v = iv(z)
            c = mul(r, v)
            a0, a1, a2, a3 = [mask(v), mask(c), mask(1), mask(mul(r, c) ^ r ^ mul(z, delta))]
            nxt = []
            for b, h in candidates:
                t0 = (b & a0).bit_count() & 1
                t1 = (b & a1).bit_count() & 1
                t2 = (b & a2).bit_count() & 1
                t3 = (b & a3).bit_count() & 1
                det = (t1 ^ t2 ^ h) & (t1 ^ h) ^ t0 & t3
                if independent and n <= 4:
                    ub = [(w, 0) for w in wb] + [(delta * h, b)]
                    cols = ub + [kmul((r, z), u) for u in ub]
                    direct = binary_rank([a ^ bb << n for a, bb in cols]) == 2 * n
                    assert direct == bool(det)
                if det:
                    nxt.append((b, h))
            assert len(nxt) == step['remaining']
            candidates = nxt
        assert not candidates
        summaries.append({'n': n, 'candidates': 2 * (q - 1), 'primitive_checks': len(cert['checks']), 'survivors': 0})
    assert {c['n'] for c in cases} == set(range(2, 19))
    return summaries
ORIGINAL_CASES = [(4, 2, 19), (6, 2, 67), (6, 3, 67), (8, 2, 285), (8, 4, 285), (9, 3, 529), (10, 2, 1033), (10, 5, 1033), (12, 2, 4179), (12, 3, 4179), (14, 2, 17475), (16, 2, 69643), (18, 2, 262273), (20, 2, 1048585)]

def original_spaces(N, n):
    for piv in combinations(range(1, N), n - 1):
        free = [(i, j) for i, p in enumerate(piv) for j in range(p + 1, N) if j not in piv]
        for mask in range(1 << len(free)):
            b = [1] + [1 << p for p in piv]
            for k, (i, j) in enumerate(free):
                if mask >> k & 1:
                    b[i + 1] ^= 1 << j
            yield b

def binary_rank(xs):
    bs = {}
    for x in xs:
        while x:
            j = x.bit_length() - 1
            if j in bs:
                x ^= bs[j]
            else:
                bs[j] = x
                break
    return len(bs)

def original_run(N, n, f):
    m = N // n
    M = (1 << N) - 1
    ex, lg, mul, iv = field(N, f)
    ds = [j for j in range(1, M) if gcd(j, M) == 1]
    cache = []

    def powers(j):
        if j == len(cache):
            beta = ex[ds[j]]
            p = [1]
            for _ in range(m - 1):
                p.append(mul(p[-1], beta))
            cache.append((ds[j], p))
        return cache[j][1]
    total = 0
    survivors = []
    started = perf_counter()
    for b in original_spaces(N, n):
        total += 1
        if all((lg[x] * ((1 << n) - 1) % M == 0 for x in b)):
            survivors.append(b)
            continue
        for j in range(len(ds)):
            ps = powers(j)
            if binary_rank([mul(x, y) for y in ps for x in b]) != N:
                break
        else:
            raise AssertionError(('Unexpected original-table survivor', N, n, b))
    expected = prod(((1 << N - 1 - i) - 1 for i in range(n - 1))) // prod(((1 << n - 1 - i) - 1 for i in range(n - 1)))
    assert total == expected and len(survivors) == 1
    result = {'N': N, 'n': n, 'm': m, 'modulus': hex(f), 'spaces': total, 'survivors': survivors, 'rejecting_exponents': [d for d, _ in cache], 'seconds': perf_counter() - started}
    print(json.dumps(result), flush=True)
    return result

def verify_examples():
    """Exact arithmetic checks for the illustrative failed reductions."""
    out = {}
    for N, f, t, beta, coefficients in [(8, 285, 36, 4, [37, 36, 0, 37]), (6, 67, 24, 35, [25, 24, 24])]:
        ex, lg, mul, iv = field(N, f)
        M = (1 << N) - 1
        assert gcd(lg[beta], M) == 1
        value = 0
        power = 1
        for c in coefficients:
            assert c in [0, 1, t, t ^ 1]
            value ^= mul(c, power)
            power = mul(power, beta)
        assert value == 0 and any(coefficients)
        entries = sorted(orbit(t, iv))
        orders = [M // gcd(lg[x], M) for x in entries]
        assert all((o < M for o in orders))
        out[str(N)] = {'t': t, 'beta': beta, 'coefficients': coefficients, 'transforms': entries, 'orders': orders}
    ex, lg, mul, iv = field(14, 17475)
    M = (1 << 14) - 1
    W = []
    for x in range(1 << 14):
        y = x
        v = 0
        for k in range(8):
            if k in [0, 1, 2, 3, 6, 7]:
                v ^= y
            y = mul(y, y)
        if v == 0:
            W.append(x)
    ws = set(W)
    assert len(ws) == 128 and 1 in ws and (252 in ws)
    assert all((mul(x, x) in ws for x in ws))
    assert gcd(lg[252], M) == 1 and lg[252] == 2090
    out['frobenius_kernel'] = {'size': len(ws), 'primitive_member': 252, 'primitive_exponent': lg[252]}
    counts = {}
    for N, f in [(4, 19), (6, 67), (8, 285)]:
        ex, lg, mul, iv = field(N, f)
        Q = 1 << N

        def direct(a, b):
            c = 0
            while b:
                if b & 1:
                    c ^= a
                a <<= 1
                if a & Q:
                    a ^= f
                b >>= 1
            return c
        for a in range(Q):
            for b in range(Q):
                assert mul(a, b) == direct(a, b)
        counts[str(N)] = Q * Q
    out['direct_polynomial_product_checks'] = counts
    return out
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, nargs='+', default=list(range(2, 11)))
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--original', action='store_true')
    parser.add_argument('--near-subfield', action='store_true')
    parser.add_argument('--engine', choices=['sets', 'bitsets'], default='sets')
    parser.add_argument('--output', default='vector_lrs_run_results.json')
    args = parser.parse_args()
    run = run_set if args.engine == 'sets' else run_bitsets
    bridge = verify_geometric_family_bridge()
    if args.original:
        result = {'original_searches': [original_run(N, n, f) for N, n, f in ORIGINAL_CASES]}
    elif args.near_subfield:
        evidence = json.loads(Path(__file__).with_name('vector_lrs_evidence.json').read_text(encoding='utf-8'))
        result = {'near_subfield_validation': verify_near_subfields(evidence['near_subfield_certificates'], independent=True)}
    elif args.validate:
        result = {'independent_validation': validate(), 'geometric_family_bridge': bridge, 'exact_examples': verify_examples()}
    else:
        moduli = {2: 19, 3: 67, 4: 285, 5: 1033, 6: 4179, 7: 17475, 8: 69643, 9: 262273, 10: 1048585}
        result = {'searches': [run(n, moduli[n]) for n in args.n], 'geometric_family_bridge': bridge}
    Path(args.output).write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Wrote', args.output)
