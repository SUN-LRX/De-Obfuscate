from pathlib import Path

text = Path("lua_test1.txt").read_text(encoding="utf-8")
idx = text.find('"LPH~')
end_idx = text.find('"', idx + 5)

after_lph = text[end_idx+1:]
print(f"After LPH~ length: {len(after_lph)}")

# Let's save the non-LPH code to a separate file so we can analyze and beautify it!
with open("work/wrapper_code.lua", "w", encoding="utf-8") as f:
    f.write(text[:idx] + '""' + after_lph)

print("Saved work/wrapper_code.lua")
