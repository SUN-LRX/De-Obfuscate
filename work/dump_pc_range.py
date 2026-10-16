import re
from pathlib import Path
from collections import defaultdict

raw = Path('work/vm_consts_indexed.log').read_bytes().decode('latin1')
records = re.findall(r'([SN]):([^:]+):([^|]*)\|E\|', raw)

proto0_fields = defaultdict(dict)
for t, path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_fields[pc][field] = (t, val)

with open('work/pc_350_580.txt', 'w', encoding='utf-8') as out:
    for pc in range(350, 580):
        if pc in proto0_fields:
            f = proto0_fields[pc]
            items = [f"{k}:{t}={v!r}" for k, (t, v) in sorted(f.items())]
            out.write(f"PC {pc:4d}: " + ", ".join(items) + "\n")

print("Done writing work/pc_350_580.txt")
