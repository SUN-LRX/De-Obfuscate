from pathlib import Path
import re

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

# Let's inspect functions defined
functions = re.findall(r'function\s*(\w*)\s*\((.*?)\)', code)
print("Functions found:")
for name, args in functions:
    print(f"  {name or '(anon)'}({args})")

# Let's look at lines around the end of file to see how execution starts
lines = code.splitlines()
print(f"Total lines in wrapper: {len(lines)}")
