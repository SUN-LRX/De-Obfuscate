import re

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    text = f.read()

loop_start = text.find("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;")
body = text[loop_start + len("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;"):].strip()

# Let's clean up the outer wrapper
# The body is a single big nested if-else tree ending before the end of while
# Let's find the matching end for the while loop
# Convert hex constants to decimal in conditions: 0X38 -> 56, etc.
def repl_hex(m):
    return str(int(m.group(0), 16))

body_dec = re.sub(r'0[xX][0-9a-fA-F]+', repl_hex, body)

# Replace lua keywords with python:
# 'then' -> ':', 'else' -> 'else:', 'elseif' -> 'elif', 'not' -> 'not ', '~=' -> '!='
# Note: In Lua: `not(iT < 56)` -> `not (iT < 56)`
# We can extract each branch path!

print("Body length:", len(body_dec))
