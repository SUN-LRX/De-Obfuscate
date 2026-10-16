import re

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find("if not(iT<0X38)then")

kw_re = re.compile(r'\b(if|do|function|while|for|repeat|until|else|elseif|end)\b')
depth = 0
matches = []

for m in kw_re.finditer(text, start):
    kw = m.group(1)
    pos = m.start()
    if kw in ('if', 'do', 'function', 'while', 'for'):
        depth += 1
    elif kw == 'repeat':
        depth += 1 # closed by until
    elif kw == 'until':
        depth -= 1
    elif kw == 'else' and depth == 1:
        print(f"Matching else found at {pos}!")
        print("Snippet:", text[pos:pos+500])
        break
    elif kw == 'elseif' and depth == 1:
        print(f"Matching elseif found at {pos}!")
    elif kw == 'end':
        depth -= 1
        if depth == 0:
            print(f"Matching end found at {pos}!")
            break
