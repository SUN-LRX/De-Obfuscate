from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

# Let's search for iV = or function iV
idx = code.find("iV")
while idx != -1:
    print(f"Match at {idx}:")
    print(code[max(0, idx-80):min(len(code), idx+150)])
    print("-" * 50)
    idx = code.find("iV", idx+2)
