from math import isqrt, gcd
from binascii import hexlify, unhexlify
from time import perf_counter

# Decimal strings are concatenated before conversion to integers.
e = int(
    "47885324298515466446776214628855983335638202654343103576613828236812"
    "219086062545569"
)

n = int(
    "37970328464789634675325450382800995937985160633271694932039830138617"
    "13169664255263865393788001512585873373119956314576055703690654535292"
    "30023765319342285073463098745982365680739537576969325080998775569316"
    "14931316742790277964249544623328399465062814447766926567907078409993"
    "38770431714571746372170728725349558017"
)

C1 = int(
    "16370438721440934664352878119037590411297615016366972146106116536204"
    "70403944965542903540790527330904378587534236991036004644943623477535"
    "34265372671255786871274286428662434604838644848585499738163720928489"
    "88530374586221211680013722693672357824587279688046021236477557771426"
    "81549705923591889045263588042807864761"
)

C2 = int(
    "35538128117877289882396355903509150341295174437568248861804565668542"
    "60845012620690086036547526446250190168850927656874469160107854944378"
    "52619471924295879928734145229524928856184485139454562589416369897821"
    "94769434822633131981403655196870182165123091079119204812045121002313"
    "99193382918006367533798052415091072350"
)

def factor_scaled_fermat(n, limit=10000):
    # Scan small ratios p/q approximately k.
    for k in range(1, limit + 1):
        a = isqrt(4*k*n)
        if a*a < 4*k*n:
            a += 1
        b2 = a*a - 4*k*n
        b = isqrt(b2)
        if b*b == b2:
            p = gcd(a-b, n)
            if 1 < p < n:
                return k, a, b, p, n//p
    raise ValueError("No factor found in this search")

def text_to_number(text):
    return int(hexlify(text.encode()), 16)

def number_to_text(m):
    return unhexlify(hex(m)[2:]).decode()

t0 = perf_counter()
k, a, b, p, q = factor_scaled_fermat(n)
phi = (p-1)*(q-1)
assert gcd(e, phi) == 1
assert p*q == n
d = pow(e, -1, phi)
M1, M2 = pow(C1, d, n), pow(C2, d, n)
text = number_to_text(M2)
assert 0 <= M1 < n and 0 <= M2 < n
assert pow(M1, e, n) == C1
assert pow(M2, e, n) == C2
assert text_to_number(text) == M2
assert M1 == C1
assert a == p + k*q and b == abs(p-k*q)
for name, val in [("k",k), ("a",a), ("b",b), ("p",p),
                  ("q",q), ("d",d), ("M1",M1), ("M2",M2)]:
    print(f"{name} = {val}")
print("Decoded text:", text)
print("All exact checks passed.")
print(f"Elapsed: {perf_counter()-t0:.4f} seconds")
