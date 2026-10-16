import re
from pathlib import Path
from collections import defaultdict

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")

# Extract all records: N:path:value|E|
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)
print(f"Total records parsed: {len(records)}")

paths = defaultdict(dict)
for p, val in records:
    paths[p] = val

print(f"Unique paths: {len(paths)}")

# Check keys under bT[7]
protos = set()
for p in paths:
    m = re.match(r'bT\[7\]\[(\d+)\]', p)
    if m:
        protos.add(int(m.group(1)))

print(f"Child prototypes under bT[7]: {sorted(protos)}")

for proto_id in sorted(protos):
    proto_paths = [p for p in paths if p.startswith(f"bT[7][{proto_id}]")]
    inst_paths = [p for p in proto_paths if f"bT[7][{proto_id}][4]" in p]
    print(f"Proto {proto_id}: total paths={len(proto_paths)}, instruction paths={len(inst_paths)}")

