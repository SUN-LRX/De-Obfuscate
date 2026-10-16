from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

# Let's search for "function gV"
idx = code.find("function gV")
if idx == -1:
    idx = code.find("gV=function")
if idx == -1:
    idx = code.find("gV = function")
if idx == -1:
    # search for gV
    matches = [i for i in range(len(code)) if code.startswith("gV", i)]
    print(f"Occurrences of gV: {matches}")
    for m in matches:
        print(f"Around {m}:")
        print(code[max(0, m-100):min(len(code), m+200)])
else:
    print("Found gV definition at", idx)
    print(code[idx:idx+1500])
