from pathlib import Path

code = Path("work/wrapper_code.lua").read_text(encoding="utf-8")
start = code.find("function VV(bT,ZT,DT)")
end = code.find("return VV(TV,d,NV)(...)", start)

vv_code = code[start:end]
print(f"VV code length: {len(vv_code)}")

with open("work/vv_interpreter.lua", "w", encoding="utf-8") as f:
    f.write(vv_code)

print("Saved work/vv_interpreter.lua")
