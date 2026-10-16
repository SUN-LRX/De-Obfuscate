import re
from pathlib import Path

code = Path("work/vv_interpreter.lua").read_text(encoding="utf-8")

# Let's find all `iT == <number>` or `iT < <number>` or `iT >= <number>`
checks = re.findall(r'iT\s*(==|<=|>=|<|>)\s*(\d+|0x[0-9a-fA-F]+)', code)
print(f"Total opcode comparisons: {len(checks)}")

# Let's extract exact cases: `if iT == <X>` or `elseif iT == <X>`
exact_ops = re.findall(r'(?:if|elseif)\s*iT\s*==\s*(\d+|0x[0-9a-fA-F]+)\s*then(.*?)(?=(?:elseif|else|end))', code, re.DOTALL)
print(f"Exact opcode matches found: {len(exact_ops)}")

op_map = {}
for op_str, body in exact_ops:
    op_num = int(op_str, 16) if op_str.startswith("0x") or op_str.startswith("0X") else int(op_str)
    # clean body
    clean_body = body.strip().replace("\n", " ")
    op_map[op_num] = clean_body[:120]

for op_num in sorted(op_map):
    print(f"Opcode {op_num:3d}: {op_map[op_num]}")
