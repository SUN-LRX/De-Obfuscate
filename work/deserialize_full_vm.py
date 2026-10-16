import struct
from pathlib import Path

# Load first-layer decoded binary
b = Path("work/decoded-rle.bin").read_bytes()
p = 0

def J():
    global p
    v = b[p]; p += 1; return v

def S():
    global p
    v = struct.unpack_from('<I', b, p)[0]; p += 4; return v

def j():
    global p
    v = struct.unpack_from('<d', b, p)[0]; p += 8; return v

def B():
    global p
    v = struct.unpack_from('<q', b, p)[0]; p += 8; return v

def k():
    global p
    v = 0; shift = 0
    while True:
        c = J()
        v |= (c & 0x7f) << shift
        if (c & 0x80) == 0:
            return v
        shift += 7

def L():
    v = k()
    return v if v < 0x80000000 else v - 0x100000000

# Read initial seeds from wrapper
o = J()
IV = J()
print(f"Initial o={o}, IV={IV}, pos={p}")

# iV function:
def iV(CD):
    global p, o
    TD = S()
    chunk = bytearray()
    BV = 7997
    pos_end = p + TD
    while p < pos_end:
        cur_len = min(BV, pos_end - p)
        raw_chunk = b[p:p+cur_len]
        p += cur_len
        dec_chunk = bytearray(len(raw_chunk))
        for i, byte_val in enumerate(raw_chunk):
            dec_chunk[i] = byte_val ^ o
            o = (CD * o + 0x6F) & 0xFF
        chunk.extend(dec_chunk)
    return bytes(chunk)

def E(val, shift, bits):
    return (val >> shift) & ((1 << bits) - 1)

def parse_proto(depth=0):
    BW = {}
    BW['proto_id'] = S()
    BW['field_C'] = J()
    iW = J()
    BW['is_vararg'] = E(iW, 1, 1) != 0
    BW['field_1'] = E(iW, 2, 1) != 0

    # Instructions
    oW = S() - 53788
    instructions = []
    for t1 in range(oW):
        # Read instruction fields in exact order of gV():
        # [5]=L(), [6]=J(), [7]=J(), [4]=L(), [3]=k(), [2]=L(), [1]=J()
        # Wait, let's verify order from gV()!
        # In gV():
        # [FV] = L()  (FV=5)
        # [6] = J()
        # [7] = J()
        # [4] = L()
        # [3] = k()
        # [2] = L()
        # [1] = J()
        f5 = L()
        f6 = J()
        f7 = J()
        f4 = L()
        f3 = k() # opcode
        f2 = L()
        f1 = J()
        instructions.append({1: f1, 2: f2, 3: f3, 4: f4, 5: f5, 6: f6, 7: f7})
    BW['instructions'] = instructions

    # Child prototypes
    KW = []
    YW = S() - 0x17a4c
    print(f"{'  '*depth}Proto at p={p}: insts={oW}, child_protos={YW}")
    for un in range(YW):
        KW.append(parse_proto(depth + 1))
    BW['child_protos'] = KW

    # Constants
    BW['field_19'] = J()
    kW = S() - 45657
    dW = J()
    CW = J() != 0
    BW['field_10'] = J()

    constants = []
    eW = {}
    aW = 1
    for fz in range(kW):
        yz = J()
        qz = None
        eW[fz] = aW
        if yz == 0xD0:
            qz = j()
        elif yz == 55:
            qz = B()
        elif yz == 0xCE:
            qz = j() + S()
        elif yz == 193:
            qz = True
        elif yz == 44:
            qz = False
        elif yz == 62:
            s_raw = iV(dW)
            qz = s_raw[3:] if len(s_raw) >= 4 else b""
        elif yz == 189:
            qz = B()
        elif yz == 0x85:
            qz = B()
        elif yz == 155:
            qz = j()
        elif yz == 209:
            start_idx = J()
            s_raw = iV(dW)
            qz = s_raw[start_idx-1:] if len(s_raw) >= start_idx else b""
        elif yz == 212:
            start_idx = int(j() + S())
            s_raw = iV(dW)
            qz = s_raw[start_idx-1:] if len(s_raw) >= start_idx else b""
        else:
            print(f"Unknown constant tag {yz} at pos {p}!")
        constants.append(qz)
        aW += 1
    BW['constants'] = constants

    # Upvalues
    MW = []
    for Zp in range(k()):
        MW.append((J(), k()))
    BW['upvalues'] = MW

    BW['field_E'] = S()
    BW['field_3'] = k()
    PW = S()
    line_records = []
    for tl in range(PW):
        Sl = S()
        il = S()
        yl = S()
        line_records.append((Sl, il, yl))
    BW['lines'] = line_records
    BW['field_2'] = k()
    BW['field_5'] = k()

    # Relocation pass
    for xE, inst in enumerate(instructions):
        # P = {4, 5, 2}
        # c = {4: 1, 5: 6, 2: 7}
        for hA, FA in [(4, 1), (5, 6), (2, 7)]:
            HA = inst[FA]
            if HA == 1:
                # Constant reference
                c_idx = inst[hA]
                if c_idx < len(constants):
                    inst[FA] = constants[c_idx]
            elif HA == 12:
                # Jump target relocation
                inst[hA] = xE + inst[hA] + 1

    return BW

try:
    root = parse_proto()
    print("SUCCESSFULLY DESERIALIZED ROOT PROTOTYPE!")
    print(f"Remaining bytes in buffer: {len(b) - p}")
except Exception as e:
    import traceback
    traceback.print_exc()
