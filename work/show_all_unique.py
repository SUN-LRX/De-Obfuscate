from pathlib import Path

strings = Path("work/extracted_all_strings.txt").read_text(encoding="utf-8").splitlines()
unique = sorted(set(s for s in strings if len(s.strip()) > 0 and s != 'nil'))

print(f"Total non-nil unique strings: {len(unique)}")
with open("work/unique_meaningful_strings.txt", "w", encoding="utf-8") as f:
    for s in unique:
        f.write(s + "\n")

print("\nAll unique strings sample:")
for s in unique[:100]:
    print(f"  {repr(s)}")
