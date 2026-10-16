from pathlib import Path

code = Path("work/vv_interpreter.lua").read_text(encoding="utf-8")
idx = code.find("local c2=(NT[LT[0X05]])")
print(code[idx-200:idx+600])
