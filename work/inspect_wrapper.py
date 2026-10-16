from pathlib import Path

text = Path("lua_test1.txt").read_text(encoding="utf-8")
idx = text.find('"LPH~')
end_idx = text.find('"', idx + 5)

print(f"Prefix length: {idx}")
print("--- Wrapper code before LPH~ ---")
print(text[:idx])
print("--- Wrapper code right after LPH~ ---")
print(text[end_idx+1:end_idx+2500])
print("--- Total length ---", len(text))
print("--- Tail of file ---")
print(text[-2000:])
