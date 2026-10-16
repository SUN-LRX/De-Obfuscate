import re
from pathlib import Path

# Read formatted loop
lines = Path("work/vv_loop_formatted.lua").read_text(encoding="utf-8").splitlines()

# We can parse the indentation and if/else structure to find for each leaf the opcode condition!
# Let's inspect the entire dispatch tree by building a path of constraints:
# A constraint is: iT < X, iT >= X, iT == X, iT ~= X, etc.

# Let's write a robust recursive descent parser for Lua AST of the dispatch loop
# Let's see: tokens
code = Path("work/vv_interpreter.lua").read_text(encoding="utf-8")
start = code.find("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;")
dispatch = code[start + len("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;"):].strip()
# Remove the trailing "end" of the while loop
if dispatch.endswith("end"):
    dispatch = dispatch[:-3].strip()

print(f"Dispatch code length: {len(dispatch)}")
