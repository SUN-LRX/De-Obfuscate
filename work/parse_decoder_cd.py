from pathlib import Path
import re

raw = Path("work/decoder_cd.log").read_bytes()
# Parse entries: CD:(\d+):L:(\d+):V:(.*?)\|E\|
entries = re.findall(rb'CD:(\d+):L:(\d+):V:(.*?)\|E\|', raw, re.DOTALL)
print(f"Total decoder entries: {len(entries)}")

for i, (cd, length, val) in enumerate(entries[:50]):
    cd_val = int(cd)
    l_val = int(length)
    # in lua: string.sub(..., 4) means val[3:] in 0-based python!
    payload = val[3:]
    printable = "".join(chr(b) if 32 <= b < 127 else f"\\x{b:02x}" for b in payload)
    print(f"{i:3d}: CD={cd_val:<4} len={l_val:<4} payload(len={len(payload)}): {printable[:60]}")
