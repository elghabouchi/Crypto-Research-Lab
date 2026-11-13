"""NSUCRYPTO 2026, Problem 7: exact transaction and Morse decoding.
Python 3.10+; standard library only. Keep the .hex file beside this file.
"""
from pathlib import Path
from hashlib import sha256

raw = bytes.fromhex(Path(__file__).with_name(
    'sherlock_problem7_transaction.hex').read_text(encoding='ascii'))
assert len(raw) == 1816
assert sha256(raw).hexdigest() == (
    '312d22d7be612a333fa24df790a35099ba738bf35db990be7c3c612a2df48af8')
patterns = ('.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. '
            '-- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..')
MORSE = dict(zip(patterns.split(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
DOT = bytes.fromhex('76a914') + bytes.fromhex('aa')*20 + bytes.fromhex('88ac')
DASH = bytes.fromhex('0014') + bytes.fromhex('bb')*20


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, n):
        assert 0 <= n <= len(self.data)-self.pos
        result = self.data[self.pos:self.pos+n]
        self.pos += n
        return result

    def uint(self, n):
        return int.from_bytes(self.take(n), 'little')

    def compact(self):
        x = self.uint(1)
        return x if x < 253 else self.uint({253: 2, 254: 4, 255: 8}[x])


def le(value, size):
    return value.to_bytes(size, 'little')


def compact(value):
    if value < 253:
        return bytes([value])
    for prefix, size in ((253, 2), (254, 4), (255, 8)):
        if value < 1 << (8*size):
            return bytes([prefix]) + le(value, size)
    raise ValueError('CompactSize overflow')


rd = Reader(raw)
version, input_count = rd.uint(4), rd.compact()
inputs = []
for _ in range(input_count):
    previous, index = rd.take(32), rd.uint(4)
    script = rd.take(rd.compact())
    inputs.append((previous, index, script, rd.uint(4)))
output_count = rd.compact()
outputs = []
for _ in range(output_count):
    value = rd.uint(8)
    outputs.append((value, rd.take(rd.compact())))
locktime = rd.uint(4)
assert rd.pos == len(raw)
assert (version, input_count, output_count, locktime) == (2, 1, 64, 0)
assert inputs == [(bytes.fromhex('11')*32, 0, b'', 0xffffffff)]

# Re-encode every field and compare all 1816 bytes exactly.
encoded = le(version, 4) + compact(input_count)
for previous, index, script, sequence in inputs:
    encoded += (previous + le(index, 4) + compact(len(script))
                + script + le(sequence, 4))
encoded += compact(output_count)
for value, script in outputs:
    encoded += le(value, 8) + compact(len(script)) + script
encoded += le(locktime, 4)
assert encoded == raw

signals, groups = [], []
start = 0
for index, (value, script) in enumerate(outputs):
    if script.startswith(bytes.fromhex('6a')):
        assert value == 0 and len(script) == 4
        assert script[:3] == bytes.fromhex('6a02ff')
        count = script[3]
        assert 1 <= count <= 4 and count == len(signals)
        pattern = ''.join(signals)
        groups.append((start, index, pattern, MORSE[pattern], count))
        signals, start = [], index+1
    else:
        assert (value, script) in ((1000, DOT), (2000, DASH))
        signals.append('.' if script == DOT else '-')
assert not signals and len(groups) == 16
assert outputs.count((1000, DOT)) == 23
assert outputs.count((2000, DASH)) == 25
assert sum(value for value, _ in outputs) == 73000
message = ''.join(group[3] for group in groups)
assert message == 'KEYISCRYPTOWORLD'
key = message.removeprefix('KEYIS')
assert key == 'CRYPTOWORLD'
print('Bytes:', len(raw), '; inputs:', input_count,
      '; outputs:', output_count, '; locktime:', locktime)
print('SHA256:', sha256(raw).hexdigest())
print('All output indices below are zero-based.')
print('Group | signal output indices | OP_RETURN index | Morse | letter')
for number, (start, end, pattern, letter, count) in enumerate(groups, 1):
    print(number, f'{start}-{end-1}', end, pattern, letter, sep=' | ')
print('Decoded message:', message)
print('ACCESS CODE:', key)
print('ALL PARSING, GROUP-LENGTH AND BYTE-ROUNDTRIP CHECKS PASSED.')
