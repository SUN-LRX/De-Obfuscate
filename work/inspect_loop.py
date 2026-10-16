import re

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    text = f.read()

# Find the main dispatch loop: while true do ... end
loop_start = text.find("while true do")
print("Loop start:", loop_start)

# Let's see lines around loop_start
snippet = text[loop_start:loop_start+2000]
print("Loop snippet:")
print(snippet)
