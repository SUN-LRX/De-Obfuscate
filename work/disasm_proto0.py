import re
from pathlib import Path
from collections import defaultdict

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0_insts = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_insts[pc][field] = val

print(f"Proto 0 total instructions: {len(proto0_insts)}")

# Let's inspect the first 40 instructions
for pc in sorted(proto0_insts.keys())[:50]:
    row = proto0_insts[pc]
    # In gV(): fields were:
    # 1: J() (mode or tag?)
    # 2: L() (operand A/B)
    # 3: k() (OPCODE!)
    # 4: L() (operand C/D)
    # 5: L() (operand E/jump)
    # 6: J()
    # 7: J()
    f1 = row.get(1, '?')
    f2 = row.get(2, '?')
    f3 = row.get(3, '?') # opcode
    f4 = row.get(4, '?')
    f5 = row.get(5, '?')
    f6 = row.get(6, '?')
    f7 = row.get(7, '?')
    print(f"PC {pc:4d}: op={f3:<5} f1={f1:<5} f2={f2:<10} f4={f4:<10} f5={f5:<10} f6={f6:<5} f7={f7:<5}")
