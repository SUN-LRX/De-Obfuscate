from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")
print(code[2300:3950])
