from pathlib import Path
import re

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

# Let's locate VV(bT, ZT, DT)
pos_vv = code.find("VV(bT,")
if pos_vv != -1:
    print("--- VV definition snippet (1500 chars) ---")
    print(code[pos_vv-50:pos_vv+1500])

# Let's locate gV()
pos_gv = code.find("gV()")
if pos_gv != -1:
    print("--- gV definition snippet (1500 chars) ---")
    print(code[pos_gv-50:pos_gv+1500])

# Let's see what is called at the end
print("--- End of wrapper_code.lua (last 1500 chars) ---")
print(code[-1500:])
