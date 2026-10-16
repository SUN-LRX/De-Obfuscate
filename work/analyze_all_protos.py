import re
from pathlib import Path
from collections import defaultdict

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto_insts = defaultdict(lambda: defaultdict(dict))

for path, val in records:
    m = re.match(r'bT\[7\]\[(\d+)\](?:\[7\]\[(\d+)\])?\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        p1 = int(m.group(1))
        p2 = m.group(2)
        key = f"Proto_{p1}" if p2 is None else f"Proto_{p1}_{p2}"
        pc = int(m.group(3))
        field = int(m.group(4))
        proto_insts[key][pc][field] = val

for proto_name, insts in sorted(proto_insts.items()):
    opcodes = [insts[pc].get(3, '?') for pc in sorted(insts.keys())]
    print(f"{proto_name}: {len(insts)} instructions, unique opcodes: {len(set(opcodes))}")
    print(f"  First 10 opcodes: {opcodes[:10]}")
