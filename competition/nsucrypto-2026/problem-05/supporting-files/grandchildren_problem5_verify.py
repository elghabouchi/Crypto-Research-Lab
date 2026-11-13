"""NSUCRYPTO 2026, Problem 5: exact checks of non-uniqueness.
Passed houses exclude the starting house and the destination.
step=1: consecutive numbering along the route.
step=2: the usual same-side even/odd numbering convention.
"""
from fractions import Fraction


def check(a, v, s, home, grandma, step):
    assert all(isinstance(x, int) and x > 0
               for x in (a, v, s, home, grandma, step))
    assert grandma == int(str(a) + str(v))
    quotients = tuple(home // age for age in (a, v, s))
    assert all(home % age == 0 for age in (a, v, s))
    difference = abs(home - grandma)
    assert difference % step == 0
    gaps = difference // step
    passed = gaps - 1
    assert passed == 16*s
    if step == 2:
        assert home % 2 == grandma % 2
    # A positive constant speed exists for a 25-minute journey.
    speed_in_gaps_per_minute = Fraction(gaps, 25)
    assert 25*speed_in_gaps_per_minute == gaps
    return dict(ages=(a, v, s), home=home, grandma=grandma,
                step=step, quotients=quotients,
                passed=passed, gaps=gaps,
                speed=str(speed_in_gaps_per_minute))


consecutive = [check(2, 9, 6, 126, 29, 1),
               check(2, 7, 7, 140, 27, 1)]
distinct_consecutive = [check(6, 13, 9, 468, 613, 1),
                        check(13, 15, 9, 1170, 1315, 1)]
same_side = [check(11, 8, 10, 440, 118, 2),
             check(15, 8, 10, 480, 158, 2)]
assert consecutive[0]['ages'] != consecutive[1]['ages']
assert same_side[0]['ages'] != same_side[1]['ages']
assert same_side[0]['ages'][1:] == same_side[1]['ages'][1:]
assert same_side[0]['gaps'] == same_side[1]['gaps'] == 161
assert same_side[0]['speed'] == same_side[1]['speed']
assert distinct_consecutive[0]['gaps'] == 145
assert distinct_consecutive[1]['gaps'] == 145
for result in consecutive + distinct_consecutive + same_side:
    print(result)
print('ALL SIX ASSIGNMENTS PASS THE STATED NUMERICAL CHECKS.')
print('The text does not determine a unique age triple or key.')
print('296 is a possible age-concatenation key, not a forced key.')
