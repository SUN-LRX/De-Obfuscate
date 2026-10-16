import re
from pathlib import Path

raw = Path("work/vm_consts.log").read_bytes()
# Extract all string entries: S:([^|]*)\|E\|
string_entries = re.findall(rb'S:([^|]*)\|E\|', raw)
print(f"Total string constants in vm_consts.log: {len(string_entries)}")

strings = []
for s in string_entries:
    try:
        text = s.decode('utf-8')
        strings.append(text)
    except:
        pass

print(f"Unique strings: {len(set(strings))}")
with open("work/extracted_all_strings.txt", "w", encoding="utf-8") as f:
    for s in strings:
        f.write(s + "\n")

print("Saved to work/extracted_all_strings.txt")
print("\nSample strings (first 80):")
for s in strings[:80]:
    if len(s) > 1:
        print(f"  {repr(s)}")
