"""Problem 10: exact checks of the proved subclasses (not the full conjecture).
Python 3.10+, standard library only. Input bits are numbered from zero.
"""
import argparse
import json
from itertools import combinations
from pathlib import Path
from random import Random


def mobius(a):
    a = list(a)
    for j in range((len(a)-1).bit_length()):
        bit = 1 << j
        for x in range(len(a)):
            if x & bit: a[x] ^= a[x ^ bit]
    return a


def truth(k, masks):
    a = [0] * (1 << k)
    for mask in masks: a[mask] ^= 1
    return mobius(a)


def degree(t):
    return max((i.bit_count() for i, a in enumerate(mobius(t)) if a),
               default=-1)


def walsh(t):
    a = [1-2*b for b in t]
    step = 1
    while step < len(a):
        for start in range(0, len(a), 2*step):
            for j in range(start, start+step):
                u, v = a[j], a[j+step]
                a[j], a[j+step] = u+v, u-v
        step *= 2
    return a


def bent(t):
    n = (len(t)-1).bit_length()
    return n % 2 == 0 and all(abs(a) == 1 << (n//2) for a in walsh(t))


def polar(t, vectors):
    points = [0]
    for v in vectors: points += [x ^ v for x in points]
    out = 0
    for x in points: out ^= t[x]
    return out


def span(basis):
    s = {0}
    for v in basis: s |= {x ^ v for x in s}
    return s


def isotropic_basis(t, k, d, target):
    assert k >= target + len(list(combinations(range(target-1), d-1)))
    z = []
    while len(z) < target:
        rows = []
        for old in combinations(z, d-1):
            rows.append(sum(polar(t, old+(1 << j,)) << j for j in range(k)))
        used = span(z)
        v = next(v for v in range(1, 1 << k) if v not in used
                 and all((v & row).bit_count() % 2 == 0 for row in rows))
        z.append(v)
    assert all(polar(t, vs) == 0 for vs in combinations(z, d))
    return z


def adapted_basis(z, k):
    used, controls = span(z), []
    for j in range(k):
        v = 1 << j
        if v not in used:
            controls.append(v)
            used |= {x ^ v for x in used}
    assert len(controls)+len(z) == k and len(used) == 1 << k
    return controls + z


def coordinate_map(basis):
    a = [0] * (1 << len(basis))
    for i in range(1, len(a)):
        b = i & -i
        a[i] = a[i ^ b] ^ basis[b.bit_length()-1]
    return a


def pack(t):
    value = sum(b << i for i, b in enumerate(t))
    return format(value, '0' + str((len(t)+3)//4) + 'x')


def quadratic_table():
    pairs = [(1 << i) | (1 << j) for i, j in combinations(range(4), 2)]
    ts = [truth(4, [a for j, a in enumerate(pairs) if mask >> j & 1])
          for mask in range(64)]
    good = [i for i, t in enumerate(ts) if bent(t)]
    assert len(good) == 28
    lookup = {q: ts[next(g for g in good if g ^ q in good)] for q in range(64)}
    return pairs, lookup


def split4(t, pairs, lookup):
    coeff = mobius(t)
    assert degree(t) <= 2
    q = sum(coeff[a] << j for j, a in enumerate(pairs))
    g = lookup[q]
    h = [a ^ b for a, b in zip(g, t)]
    assert bent(g) and bent(h)
    return g, h


def base_checks(pairs, lookup):
    monos = [i for i in range(16) if i.bit_count() <= 2]
    for mask in range(1 << len(monos)):
        t = truth(4, [a for j, a in enumerate(monos) if mask >> j & 1])
        split4(t, pairs, lookup)
    print('BASE: all 2048 degree-at-most-2 functions on 4 variables checked.')


def cubic_checks(rng, pairs, lookup, count=256):
    monos = [i for i in range(128) if i.bit_count() <= 3]
    certificate = None
    for case in range(count):
        masks = [a for a in monos if rng.getrandbits(1)]
        f = truth(7, masks)
        z = isotropic_basis(f, 7, 3, 4)
        basis = adapted_basis(z, 7)
        mp = coordinate_map(basis)
        slices = [split4([f[mp[u | (s << 3)]] for s in range(16)],
                         pairs, lookup) for u in range(8)]
        g, h = [], []
        for x in range(1024):
            u, s, v = x & 7, (x >> 3) & 15, x >> 7
            dot = (u & v).bit_count() % 2
            a, b = slices[u]
            g.append(dot ^ a[s]); h.append(dot ^ b[s])
            assert g[-1] ^ h[-1] == f[mp[x & 127]]
        assert bent(g) and bent(h)
        if case == 0:
            certificate = dict(n=10, active_anf_masks=masks,
                               control_then_z_basis=basis,
                               coordinate_order='u:3 low bits, z:4, v:3 high bits',
                               g_truth_hex=pack(g), h_truth_hex=pack(h))
    print(f'CUBIC: {count} deterministic random 7-variable cubics lifted to 10 variables;')
    print('       every decomposition checked pointwise; every Walsh coefficient is +/-32.')
    return certificate


def quartic_checks(rng, count=8):
    monos = [sum(1 << j for j in c) for c in combinations(range(16), 4)]
    for _ in range(count):
        f = truth(16, [a for a in monos if rng.getrandbits(1)])
        z = isotropic_basis(f, 16, 4, 6)
        mp = coordinate_map(adapted_basis(z, 16))
        for u in range(1024):
            assert degree([f[mp[u | (s << 10)]] for s in range(64)]) <= 3
    print(f'QUARTIC: {count} deterministic random quartic forms on 16 variables;')
    print(f'         six-dimensional isotropic spaces found; all {count*1024} slices have degree <=3.')
    print('         This check does not compute Walsh spectra on 26 variables.')


def example8():
    f, g, h = [], [], []
    for a in range(256):
        u, v = a & 1, (a >> 1) & 1
        x = [(a >> (j+2)) & 1 for j in range(3)]
        y = [(a >> (j+5)) & 1 for j in range(3)]
        qi = sum(s*t for s, t in zip(x, y)) % 2
        qm = (x[0]*y[2] ^ x[1]*y[0] ^ x[1]*y[2] ^ x[2]*y[1])
        term = u*x[0]*x[1]*x[2]
        f.append(qi ^ term)
        g.append(u*v ^ qm ^ term)
        h.append(u*v ^ qm ^ qi)
    assert all(a ^ b == c for a, b, c in zip(g, h, f))
    assert bent(g) and bent(h)
    assert [degree(t) for t in (f, g, h)] == [4, 4, 2]
    print('EXAMPLE: 8-variable quartic; degrees (f,g,h)=(4,4,2); Walsh(g), Walsh(h)=+/-16.')
    return dict(n=8, coordinate_order='u,v,x1,x2,x3,y1,y2,y3 (low to high bits)',
                f_truth_hex=pack(f), g_truth_hex=pack(g), h_truth_hex=pack(h))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificates', type=Path)
    args = parser.parse_args()
    rng = Random(20261019)
    pairs, lookup = quadratic_table()
    base_checks(pairs, lookup)
    example = example8()
    cubic = cubic_checks(rng, pairs, lookup)
    quartic_checks(rng)
    if args.certificates:
        args.certificates.write_text(json.dumps(dict(
            truth_encoding='bit i of the hexadecimal integer is the value at input i',
            explicit_quartic8=example, sampled_cubic10=cubic), indent=2), encoding='utf-8')
    print('PASS. Sampled checks supplement the proofs; the full conjecture is not resolved.')


if __name__ == '__main__':
    main()
