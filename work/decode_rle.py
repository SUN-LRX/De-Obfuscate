import re
from pathlib import Path

src = Path(r"C:\Users\kvsti\OneDrive\Desktop\Test1\lua_test1.txt").read_text(encoding="utf-8")
m = re.search(r'"(LPH~.*?)"', src, re.S)
enc = m.group(1)[4:]
out = bytearray()
i = 0
pending = None
while i < len(enc):
    pair = enc[i:i+2]
    i += 2
    if len(pair) < 2:
        break
    if pair[1] == "H":
        pending = int(pair[0], 16)
        continue
    b = int(pair, 16)
    out.extend(bytes([b]) * (pending if pending is not None else 1))
    pending = None
Path("work/decoded-rle.bin").write_bytes(out)
print(f"encoded={len(enc)} decoded={len(out)} pending={pending}")
print(out[:128])

alt = bytearray(); i = 0; pending = None; last = None
while i < len(enc):
    pair = enc[i:i+2]; i += 2
    if len(pair) < 2: break
    if pair[1] == "H":
        pending = int(pair[0], 16); continue
    v = int(pair, 16)
    if pending is not None and last is not None:
        alt.extend(bytes([last]) * pending)
        pending = None
    alt.append(v); last = v
Path("work/decoded-rle-alt.bin").write_bytes(alt)
print(f"alternate decoded={len(alt)} first={alt[:32]}")
