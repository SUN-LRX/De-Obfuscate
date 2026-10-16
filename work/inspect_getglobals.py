import re
from pathlib import Path

# Load decoder_cd.log
raw_cd = Path("work/decoder_cd.log").read_bytes()
cd_entries = re.findall(rb'CD:(\d+):L:(\d+):V:(.*?)\|E\|', raw_cd, re.DOTALL)
print(f"Total decoder_cd entries: {len(cd_entries)}")

# Clean decoder strings
dec_strings = []
for cd, l, val in cd_entries:
    # skip 3 bytes
    payload = val[3:]
    dec_strings.append(payload)

# Let's see: In Proto 0, how are strings referenced?
# Let's look at GETGLOBAL instructions in Proto 0:
# PC 5: GETGLOBAL r0 = _ENV[1]
# PC 9: GETGLOBAL r178 = _ENV[10]
# PC 19: GETGLOBAL r60 = _ENV[-3624381080]
# Let's inspect all GETGLOBAL and GETTABLE_K instructions in Proto 0:
raw_idx = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw_idx)

proto0_insts = {}
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        f = int(m.group(2))
        if pc not in proto0_insts:
            proto0_insts[pc] = {}
        proto0_insts[pc][f] = val

getglobals = []
for pc, fields in sorted(proto0_insts.items()):
    op = fields.get(3)
    if op == '3': # GETGLOBAL
        key = fields.get(6)
        dest = fields.get(2)
        getglobals.append((pc, dest, key))

print(f"Total GETGLOBAL instructions in Proto 0: {len(getglobals)}")
print("Sample GETGLOBAL:")
for pc, dest, key in getglobals[:30]:
    print(f"PC {pc:4d}: dest=r{dest} key={key}")
