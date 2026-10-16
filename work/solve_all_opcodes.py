import re
import sys
from pathlib import Path

def strip_strings_comments(lua_code):
    lua_code = re.sub(r'--\[(=*)\[.*?\]\1\]', '', lua_code, flags=re.DOTALL)
    lua_code = re.sub(r'--[^\n]*', '', lua_code)
    lua_code = re.sub(r'\[(=*)\[.*?\]\1\]', '""', lua_code, flags=re.DOTALL)
    lua_code = re.sub(r'"(?:\\.|[^"\\])*"', '""', lua_code)
    lua_code = re.sub(r"'(?:\\.|[^'\\])*'", "''", lua_code)
    return lua_code

with open("work/vv_interpreter.lua", "r", encoding="utf-8") as f:
    raw = f.read()

clean = strip_strings_comments(raw)
start = clean.find("if not(iT<0X38)then")

# Tokenize into keywords and code chunks
token_re = re.compile(r'\b(if|then|else|elseif|end|do|while|for|repeat|until|function)\b')
tokens = []
last_pos = start

for m in token_re.finditer(clean, start):
    text_before = clean[last_pos:m.start()].strip()
    if text_before:
        tokens.append(('CODE', text_before, last_pos, m.start()))
    tokens.append((m.group(1), m.group(1), m.start(), m.end()))
    last_pos = m.end()

text_after = clean[last_pos:].strip()
if text_after:
    tokens.append(('CODE', text_after, last_pos, len(clean)))

pos = 0

def parse_stmts():
    global pos
    stmts = []
    while pos < len(tokens):
        t_type, t_val, s_pos, e_pos = tokens[pos]
        if t_type in ('else', 'elseif', 'end', 'until'):
            break
        elif t_type in ('while', 'for'):
            # consumes while/for ... do ... end
            w_type = t_type
            pos += 1
            # scan to 'do'
            while pos < len(tokens) and tokens[pos][0] != 'do':
                pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'do':
                pos += 1
            body = parse_stmts()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.append(('LOOP', w_type, body))
        elif t_type == 'repeat':
            pos += 1
            body = parse_stmts()
            if pos < len(tokens) and tokens[pos][0] == 'until':
                pos += 1
                # next might be condition
                if pos < len(tokens) and tokens[pos][0] == 'CODE':
                    pos += 1
            stmts.append(('REPEAT', body))
        elif t_type == 'function':
            pos += 1
            body = parse_stmts()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.append(('FUNC', body))
        elif t_type == 'do':
            pos += 1
            body = parse_stmts()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.extend(body)
        elif t_type == 'if':
            pos += 1
            # scan cond until 'then'
            cond_parts = []
            while pos < len(tokens) and tokens[pos][0] != 'then':
                cond_parts.append(tokens[pos][1])
                pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'then':
                pos += 1
            cond_str = " ".join(cond_parts).strip()
            then_branch = parse_stmts()
            else_branch = []
            if pos < len(tokens) and tokens[pos][0] == 'else':
                pos += 1
                else_branch = parse_stmts()
            elif pos < len(tokens) and tokens[pos][0] == 'elseif':
                # Treat elseif as else if
                tokens[pos] = ('if', 'if', tokens[pos][2], tokens[pos][3])
                else_branch = parse_stmts()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.append(('IF', cond_str, then_branch, else_branch))
        elif t_type == 'CODE':
            stmts.append(('CODE', raw[s_pos:e_pos]))
            pos += 1
        else:
            pos += 1
    return stmts

ast = parse_stmts()
print(f"Parsed root statements: {len(ast)}")

def eval_cond(cond_str, iT_val):
    s = re.sub(r'0[xX][0-9a-fA-F]+', lambda m: str(int(m.group(0), 16)), cond_str)
    if 'iT' in s:
        # replace lua ~= with !=
        s_py = s.replace('~=', '!=').replace('iT', str(iT_val))
        try:
            return bool(eval(s_py, {"__builtins__": {}}, {}))
        except Exception:
            return None
    return None

def solve_for_op(node_list, iT_val):
    results = []
    for node in node_list:
        n_type = node[0]
        if n_type == 'CODE':
            results.append(node[1])
        elif n_type in ('LOOP', 'REPEAT', 'FUNC'):
            results.append(f"{n_type}({solve_for_op(node[2] if n_type=='LOOP' else node[1], iT_val)})")
        elif n_type == 'IF':
            _, cond, then_b, else_b = node
            res = eval_cond(cond, iT_val)
            if res is True:
                results.extend(solve_for_op(then_b, iT_val))
            elif res is False:
                results.extend(solve_for_op(else_b, iT_val))
            else:
                results.append(f"IF({cond}) -> THEN: {solve_for_op(then_b, iT_val)} ELSE: {solve_for_op(else_b, iT_val)}")
    return results

op_table = {}
for op in range(0, 112):
    code_pieces = solve_for_op(ast, op)
    full_code = " ".join(code_pieces).strip()
    # clean up
    clean_code = re.sub(r'\s+', ' ', full_code)
    op_table[op] = clean_code

with open("work/resolved_opcodes.txt", "w", encoding="utf-8") as f:
    for op in sorted(op_table.keys()):
        f.write(f"OP {op:3d}: {op_table[op]}\n")

print("Saved work/resolved_opcodes.txt")
