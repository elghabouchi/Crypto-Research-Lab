"""NSUCRYPTO 2026, Problem 8: exact RSA verification (Python 3.8+)."""
from math import gcd, isqrt

# DDMMYYYY birthdays: Gauss, then Vigenere (leading zero omitted).
p, q, e = 30041777, 5041523, 65537

def is_prime(n):
    return n >= 2 and all(n % t for t in range(2, isqrt(n) + 1))

assert is_prime(p) and is_prime(q) and p != q
n = p * q
phi = (p - 1) * (q - 1)
assert gcd(e, phi) == 1
d = pow(e, -1, phi)
assert e * d % phi == 1

# Entries are listed in recovered reading order, not geometric order.
blocks = [
    ("Left book 1", "69cac604f3f6"),
    ("Left book 2", "0037e3e277d0"),
    ("Left book 3", "5bf4286560fd"),
    ("Left book 4", "7a78ae829dee"),
    ("Left drawer", "1160d891335b"),
    ("Right book 1", "25aa4a80579b"),
    ("Right book 2", "465d1f5ae113"),
    ("Right book 3", "3f268417e1bd"),
    ("Right book 4", "751fb3515b44"),
    ("Right box", "44a174ad7278"),
    ("Left scroll", "660301648837"),
    ("Hat", "7a8d796a70ab"),
    ("Open book", "5c40bf50d20b"),
    ("Paper by cup", "3932ff60773e"),
    ("Top frame", "8649d2897de8"),
    ("Map", "1d5a29213b82"),
    ("Front note", "788f5bae6242"),
]
assert len(blocks) == len({s for _, s in blocks}) == 17
print(f"p = {p}; q = {q}; e = {e}")
print(f"n = {n}; phi = {phi}; d = {d}")
print(f"e*d - 1 = {(e*d-1)//phi} * phi")
plain = []
for i, (place, h) in enumerate(blocks, 1):
    c = int(h, 16)
    assert 0 <= c < n
    m = pow(c, d, n)
    assert 0 <= m < 2**32
    chunk = m.to_bytes(4, "big")
    assert all(32 <= b <= 126 for b in chunk)
    assert pow(int.from_bytes(chunk, "big"), e, n) == c
    plain.append(chunk)
    print(f"{i:2} {place:14} {h} {m:10} {chunk!r}")
message = b"".join(plain)
expected = b'"Cryptography is typically bypassed, not penetrated." - Adi Shamir  '
assert message == expected
print("Recovered 68 bytes:", repr(message.decode("ascii")))
print("All 17 original hexadecimal blocks reproduced exactly.")
print("Both primes verified by exhaustive trial division.")
