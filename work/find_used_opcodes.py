import re
from pathlib import Path

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    code = f.read()

# Let's find the loop
start = code.find("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;")
dispatch = code[start + len("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;"):]

# We want to extract for each opcode what code runs.
# Let's tokenize dispatch into keywords and code chunks:
# We can use a recursive descent parser for:
# Stmt -> if Cond then Stmt else Stmt end | Stmt ; Stmt | Action

# Let's inspect the unique opcodes that appear in Proto_0, Proto_1, and Root (instruction_table.log)
from collections import Counter

table_raw = Path("work/instruction_table.log").read_bytes().decode("latin1")
table_ops = set()
for m in re.finditer(r'I:\d+:(?:[^:]+:){2}(\d+):', table_raw):
    table_ops.add(int(m.group(1)))

print("Root instruction table unique opcodes:", sorted(table_ops))

# Let's also check Proto_0 opcodes from vm_consts_indexed.log
raw_idx = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
proto0_ops = set()
for m in re.finditer(r'bT\[7\]\[0\]\[4\]\[\d+\]\[3\]:(\d+)\|E\|', raw_idx):
    proto0_ops.add(int(m.group(1)))

print("Proto 0 unique opcodes:", sorted(proto0_ops))
all_ops = sorted(table_ops | proto0_ops)
print(f"Total distinct opcodes used across Root and Proto 0: {len(all_ops)}")
print("All ops:", all_ops)
