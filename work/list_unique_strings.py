import re
from pathlib import Path

data = Path("work/vm_consts.log").read_bytes()
strings = re.findall(rb'N:([^|]+)\|E\|', data)

unique_strings = set()
for s in strings:
    try:
        text = s.decode('utf-8')
        if len(text) >= 2 and any(c.isalpha() for c in text):
            unique_strings.add(text)
    except:
        pass

print(f"Total unique words/strings: {len(unique_strings)}")
for s in sorted(unique_strings):
    print(s)
