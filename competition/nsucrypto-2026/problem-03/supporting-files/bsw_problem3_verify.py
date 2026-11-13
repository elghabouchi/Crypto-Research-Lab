"""Exact exhaustive verification for NSUCRYPTO 2026, Problem 3.
Python 3.10+; standard library only. No heuristic or search cutoff.
Usage: python bsw_problem3_verify.py [43 47 ...]
       python bsw_problem3_verify.py controls
"""
from math import isqrt
from time import perf_counter
import json
import sys

CASES = (43, 47, 59, 67, 71, 79, 83, 103, 107, 127)
CONTROLS = {7: 2, 11: 7, 19: 45, 23: 110, 31: 16}
EXPECTED_NODES = (2027, 2646, 7686, 12492, 15750,
                  29440, 35270, 107545, 125518, 298945)


def verify(q):
    assert q > 2 and q % 2 == 1
    assert all(q % d for d in range(2, isqrt(q) + 1))
    start = perf_counter()
    sq = sorted({a*a % q for a in range(1, q)})
    ns = sorted(set(range(1, q)) - set(sq))
    m = len(sq)
    chi = [0] + [1 if a in sq else -1 for a in range(1, q)]
    pairs = [(s, t) for s in sq for t in ns]
    rows = [((1 << m) - 1) << (i*m) for i in range(m)]
    adjacency = []
    for s, t in pairs:
        mask = 0
        for j, (u, v) in enumerate(pairs):
            if chi[((s-u)*(s-v)*(t-u)*(t-v)) % q] == -1:
                mask |= 1 << j
        adjacency.append(mask)
    nodes = total = nonstandard = 0
    parameters = {}
    leaves_by_depth = [0]*(m+1)

    def check_leaf(chosen):
        # Independently check every hypothesis in the original statement.
        psi = {}
        for index in chosen:
            s, t = pairs[index]
            assert s not in psi and t not in psi
            psi[s], psi[t] = t, s
        assert set(psi) == set(range(1, q))
        for x in range(1, q):
            assert psi[psi[x]] == x
            assert chi[psi[x]] == -chi[x]
            for y in range(1, q):
                if y in (x, psi[x]):
                    continue
                factors = (x-y, x-psi[y], psi[x]-y, psi[x]-psi[y])
                value = 1
                for a in factors:
                    value = value*a % q
                assert chi[value] == -1
        return {s*t % q for s, t in (pairs[i] for i in chosen)}

    def search(candidates, remaining, chosen):
        nonlocal nodes, total, nonstandard
        nodes += 1
        leaves_by_depth[len(chosen)] += 1
        if not remaining:
            products = check_leaf(chosen)
            total += 1
            if len(products) == 1:
                a = next(iter(products))
                parameters[a] = parameters.get(a, 0) + 1
            else:
                nonstandard += 1
            return
        # Choose a constrained square; stop early at zero or one option.
        best, size, row = 0, m+1, -1
        for r in remaining:
            options = candidates & rows[r]
            count = options.bit_count()
            if count < size:
                best, size, row = options, count, r
                if size <= 1:
                    break
        if size == 0:
            return
        rest = [r for r in remaining if r != row]
        while best:
            bit = best & -best
            best -= bit
            index = bit.bit_length() - 1
            search(candidates & adjacency[index], rest,
                   chosen + [index])

    search((1 << (m*m))-1, list(range(m)), [])
    # Confirm exactly one standard map for every nonsquare parameter.
    assert parameters == {a: 1 for a in ns}
    if q in CASES:
        assert total == m and nonstandard == 0
        assert nodes == EXPECTED_NODES[CASES.index(q)]
    if q in CONTROLS:
        assert nonstandard == CONTROLS[q]
    result = dict(q=q, vertices=m*m, nodes=nodes,
                  solutions=total, standard=len(parameters),
                  nonstandard=nonstandard,
                  parameters=sorted(parameters),
                  calls_by_depth=leaves_by_depth,
                  seconds=round(perf_counter()-start, 6))
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    args = sys.argv[1:]
    if args == ['controls']:
        inputs = tuple(CONTROLS)
    else:
        inputs = tuple(map(int, args)) if args else CASES
    results = [verify(q) for q in inputs]
    print('ALL CHECKS PASSED', flush=True)
