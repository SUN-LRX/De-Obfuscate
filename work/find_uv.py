from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")

matches = [i for i in range(len(code)) if code.startswith("UV", i)]
print("Matches for UV:", matches)
for m in matches:
    print(code[max(0, m-50):min(len(code), m+100)])
    print("-" * 40)
