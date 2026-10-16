from pathlib import Path
import re

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

# Let's inspect everything between Z = ... and TV = gV()
start = code.find('Z=a(g(Z,FV),"..",function(A4)')
end = code.find('TV=gV()')
print(f"Start: {start}, End: {end}")
print(code[start:start+1500])
print("="*60)
print(code[end-1500:end+100])
