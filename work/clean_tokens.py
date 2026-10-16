import re

def strip_strings_comments(lua_code):
    # Remove single-line comments: --[^\n]*
    # Remove multi-line comments: --\[(=*)\[.*?\]\1\]
    lua_code = re.sub(r'--\[(=*)\[.*?\]\1\]', '', lua_code, flags=re.DOTALL)
    lua_code = re.sub(r'--[^\n]*', '', lua_code)
    # Remove multi-line strings: \[(=*)\[.*?\]\1\]
    lua_code = re.sub(r'\[(=*)\[.*?\]\1\]', '""', lua_code, flags=re.DOTALL)
    # Remove single-quoted and double-quoted strings (handling escapes):
    lua_code = re.sub(r'"(?:\\.|[^"\\])*"', '""', lua_code)
    lua_code = re.sub(r"'(?:\\.|[^'\\])*'", "''", lua_code)
    return lua_code

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    raw = f.read()

clean = strip_strings_comments(raw)
start = clean.find("if not(iT<0X38)then")

kw_re = re.compile(r'\b(if|do|function|while|for|repeat|until|else|elseif|end)\b')
depth = 0
matches = []
for i, m in enumerate(kw_re.finditer(clean, start)):
    kw = m.group(1)
    if kw in ('if', 'do', 'function', 'while', 'for'): depth += 1
    elif kw == 'repeat': depth += 1
    elif kw == 'until': depth -= 1
    elif kw == 'end': depth -= 1
    if depth == 1 and kw in ('else', 'elseif'):
        print(f"Found {kw} at depth 1, pos {m.start()}!")
        print("Raw code snippet:")
        print(clean[m.start():m.start()+300])
    if depth == 0:
        print(f"Found matching end at pos {m.start()}!")
        break
