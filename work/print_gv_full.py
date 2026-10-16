from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")
start = code.find("function gV()")
end = code.find("return BW;end", start)
print(code[start:end+15])
