import re
from pathlib import Path

for name in ['work/vm_consts_indexed.log', 'work/vm_consts.log']:
    data = Path(name).read_bytes()
    # Find readable strings
    strings = re.findall(b'N:[^:]*:([^|]+)\|E\|', data)
    printable = []
    for s in strings:
        if len(s) >= 3 and all(32 <= b < 127 for b in s):
            text = s.decode('ascii')
            if not text.isdigit() and not (text.startswith('-') and text[1:].isdigit()):
                printable.append(text)
    print(f"=== {name} ===")
    print(f"Total string records: {len(strings)}, printable non-numeric: {len(printable)}")
    print("Sample:", printable[:40])
