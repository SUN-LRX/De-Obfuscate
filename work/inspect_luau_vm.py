import struct
from pathlib import Path

b = Path('work/decoded-rle.bin').read_bytes()
p = 0

def J():
    global p
    v = b[p]; p += 1; return v
def S():
    global p
    v = struct.unpack_from('<I', b, p)[0]; p += 4; return v
def D():
    global p
    v = struct.unpack_from('<d', b, p)[0]; p += 8; return v
def B():
    global p
    v = struct.unpack_from('<q', b, p)[0]; p += 8; return v
def K():
    v = 0; shift = 0
    while True:
        c = J(); v |= (c & 0x7f) << shift
        if c & 0x80 == 0: return v
        shift += 7
def L():
    v = K(); return v if v <= 0x080000000-1 else v - 0x100000000

print('decoded bytes', len(b), 'initial', b[:16].hex())
o = J(); iv = J()
print('decoder seeds', o, iv, 'position', p)
print('next bytes', b[p:p+32].hex())

# Parse the constant-table prelude of gV(), enough to expose any plaintext
# numeric/boolean/string-adjacent values without running the VM.
proto_id = S(); flags = J()
iW = J()
oW = S() - 53788
print('constant count', oW, 'iW', iW, 'position', p)
constants = []
for n in range(oW):
    vals = [L(), L(), J(), J(), L(), K(), L(), J()]
    constants.append(vals)
print('constant prelude parsed at', p)
for n, vals in enumerate(constants[:40], 1):
    print(n, vals)

print('first prototype id/flags', proto_id, flags, 'position', p)
print('next bytes', b[p:p+32].hex())
