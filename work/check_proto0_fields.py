import re
from pathlib import Path

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

non_inst_0 = [p for p, val in records if p.startswith("bT[7][0]") and not p.startswith("bT[7][0][4]")]
print("Non-instruction paths for Proto 0:")
for p in non_inst_0:
    for path, val in records:
        if path == p:
            print(f"  {p} = {val}")
            break

# Also check Proto 1
non_inst_1 = [p for p, val in records if p.startswith("bT[7][1]") and not p.startswith("bT[7][1][4]")]
print("\nNon-instruction paths for Proto 1:")
for p in non_inst_1[:30]:
    for path, val in records:
        if path == p:
            print(f"  {p} = {val}")
            break
