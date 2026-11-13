"""NSUCRYPTO 2026, Problem 6: exact rotating-grille solution.
Python 3.10+; standard library only. Spaces are significant.
Run normally for verification; add --recover for full grille recovery.
"""
from collections import Counter
from itertools import product
import sys

KNOWN_TEXT = (
    'How can I prove to you that I know secret word,without'
    ' ever whispering a single syllable of the word itself?'
)

KNOWN_CIPHER = (
    'H I o  ypokwrovu  tcanowhen   saItotesp cdee,vrrwitere'
    ' t ingwhw ooahruti d fsyi lttilabhen glselwlef e?os or'
)

REPLY_CIPHER = (
    'B odlmeenyl  y  asthaa tkrtiihengd  sr nsd wkeeecepcre'
    'r,fouitlod ngwoa rm astis yo w Ikuthaytlonsuodhowute!s'
)

EXPECTED_REPLY = (
    'By asking me a riddle that only the secret word coulda'
    'nswer,for keeping mouthshut is loudest waytosay Iknow!'
)

HOLES = (0, 4, 11, 17, 19, 20, 26, 28, 32)


def rotate(i):
    return (i % 6)*6 + 5 - i//6


def transpose(i):
    return (i % 6)*6 + i//6


def order(holes):
    result = []
    for _ in range(4):
        result.extend(sorted(holes))
        holes = tuple(map(rotate, holes))
    assert sorted(result) == list(range(36))
    return result


def encrypt(text, holes):
    assert len(text) % 36 == 0
    visit = order(holes)
    output = []
    for offset in range(0, len(text), 36):
        grid = ['']*36
        for j, i in enumerate(visit):
            grid[i] = text[offset+j]
        output.extend(grid)
    return ''.join(output)


def decrypt(cipher, holes):
    assert len(cipher) % 36 == 0
    visit = order(holes)
    return ''.join(cipher[offset+i]
                   for offset in range(0, len(cipher), 36)
                   for i in visit)


def recover():
    # A valid grille chooses one cell from each 90-degree orbit.
    orbits, used = [], set()
    for i in range(36):
        if i in used:
            continue
        orbit, j = [], i
        for _ in range(4):
            orbit.append(j)
            j = rotate(j)
        used.update(orbit)
        orbits.append(tuple(sorted(orbit)))
    assert len(orbits) == 9 and len(used) == 36
    matches = []
    tested = 0
    for choice in product(*orbits):
        tested += 1
        holes = tuple(sorted(choice))
        # Check the first nine filled positions in all three blocks.
        if any(KNOWN_TEXT[36*b+j] != KNOWN_CIPHER[36*b+i]
               for j, i in enumerate(holes) for b in range(3)):
            continue
        if encrypt(KNOWN_TEXT, holes) == KNOWN_CIPHER:
            matches.append(holes)
    assert tested == 4**9
    assert matches == [HOLES]
    print('Grilles tested:', tested, '; unique match:', matches[0])


assert len(KNOWN_TEXT) == len(KNOWN_CIPHER) == 108
assert len(REPLY_CIPHER) == len(EXPECTED_REPLY) == 108
assert Counter(KNOWN_TEXT) == Counter(KNOWN_CIPHER)
assert all(Counter(KNOWN_TEXT[i:i+36]) ==
           Counter(KNOWN_CIPHER[i:i+36]) for i in (0, 36, 72))
MIRROR = tuple(sorted(map(transpose, HOLES)))
assert encrypt(KNOWN_TEXT, HOLES) == KNOWN_CIPHER
assert decrypt(KNOWN_CIPHER, HOLES) == KNOWN_TEXT
reply = decrypt(REPLY_CIPHER, MIRROR)
assert reply == EXPECTED_REPLY
assert encrypt(reply, MIRROR) == REPLY_CIPHER
if '--recover' in sys.argv[1:]:
    recover()
print('Exact reply:', repr(reply))
print('Initial grille, zero-based cells:', HOLES)
print('Reply grille, zero-based cells:', MIRROR)
print('ALL EXACT ENCRYPTION AND DECRYPTION CHECKS PASSED.')
