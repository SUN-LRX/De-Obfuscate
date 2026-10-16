import re
from pathlib import Path
from collections import defaultdict

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0_fields = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_fields[pc][field] = val

coords = []
for pc in sorted(proto0_fields):
    f6 = proto0_fields[pc].get(6, '')
    f3 = proto0_fields[pc].get(3, '')
    try:
        val = float(f6)
        if '.' in f6:
            coords.append((pc, f3, val))
    except:
        pass

print(f"Total float constants in Proto 0: {len(coords)}")
for pc, op, val in coords:
    print(f"PC {pc:4d} (op {op}): {val}")
