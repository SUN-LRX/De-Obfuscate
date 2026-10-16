import re

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    text = f.read()

loop_start = text.find("while true do")
# The loop ends at the outer while end
loop_code = text[loop_start:]

# Let's write a tokenizer/lexer for Lua syntax in this dispatch loop
tokens = []
# We care about: if, not, then, else, elseif, end, iT, <, <=, >, >=, ==, ~=, numbers, identifiers, do, while, repeat, until, etc.
pattern = re.compile(r'''
    (\-\-.*?$) |                         # comments
    (0x[0-9a-fA-F]+|\d+) |               # numbers
    (<=|>=|==|~=|<|>) |                  # comparisons
    (\b(?:if|then|else|elseif|end|not|do|while|repeat|until|local|function|return)\b) | # keywords
    (\b[a-zA-Z_]\w*\b) |                 # identifiers
    ([(),{}[\];=+\-*/%^#]) |             # operators/punctuation
    (".*?"|'.*?')                        # strings
''', re.VERBOSE | re.MULTILINE)

# Let's save a clean formatted version of loop_code with indentation to work/vv_loop_formatted.lua
# A simple regex-based formatter:
indent = 0
formatted = []
for line in loop_code.replace(";", ";\n").replace("then", "then\n").replace("else", "\nelse\n").replace("end", "\nend\n").splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith("end") or line.startswith("else"):
        indent = max(0, indent - 1)
    formatted.append("  " * indent + line)
    if line.endswith("then") or line.startswith("else") or line.endswith("do"):
        indent += 1

with open("work/vv_loop_formatted.lua", "w", encoding="utf-8") as f:
    f.write("\n".join(formatted))

print(f"Formatted lines: {len(formatted)}")
