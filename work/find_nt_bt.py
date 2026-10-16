from pathlib import Path
import re

code = Path("work/vv_interpreter.lua").read_text(encoding="utf-8")

matches = re.finditer(r'\bNT\[[^\]]+\]', code)
print("Occurrences of NT[...]:")
for m in matches:
    idx = m.start()
    print(code[max(0, idx-40):min(len(code), idx+100)])
    print("-" * 50)

matches_bt = re.finditer(r'\bbT\[[^\]]+\]', code)
print("Occurrences of bT[...]:")
for m in matches_bt:
    idx = m.start()
    print(code[max(0, idx-40):min(len(code), idx+100)])
    print("-" * 50)
