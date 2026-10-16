import re
from pathlib import Path

code = Path("work/vv_interpreter.lua").read_text(encoding="utf-8")
start = code.find("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;")
dispatch = code[start + len("while true do local LT=(jT[jH]);local iT=(LT[3]);jH=jH+1;"):].strip()
if dispatch.endswith("end"):
    dispatch = dispatch[:-3].strip()

# Let's tokenize dispatch into:
# Keywords: 'if', 'then', 'else', 'elseif', 'end', 'do'
# And tokens between them
# Notice 'do ... end' blocks might appear.
# Let's write a token stream:
token_pattern = re.compile(r'\b(if|then|else|elseif|end|do)\b')

tokens = []
last_pos = 0
for m in token_pattern.finditer(dispatch):
    text_before = dispatch[last_pos:m.start()].strip()
    if text_before:
        tokens.append(('CODE', text_before))
    tokens.append((m.group(1), m.group(1)))
    last_pos = m.end()

text_after = dispatch[last_pos:].strip()
if text_after:
    tokens.append(('CODE', text_after))

print(f"Total tokens: {len(tokens)}")

# Recursive parser:
pos = 0

def parse_block():
    global pos
    stmts = []
    while pos < len(tokens):
        t_type, t_val = tokens[pos]
        if t_type in ('else', 'elseif', 'end'):
            break
        elif t_type == 'do':
            pos += 1
            inner = parse_block()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.extend(inner)
        elif t_type == 'if':
            pos += 1
            # Next token should be condition (CODE)
            cond = ""
            while pos < len(tokens) and tokens[pos][0] != 'then':
                cond += " " + tokens[pos][1]
                pos += 1
            if pos < len(tokens) and tokens[pos][0] == 'then':
                pos += 1
            then_body = parse_block()
            else_body = []
            if pos < len(tokens) and tokens[pos][0] == 'else':
                pos += 1
                else_body = parse_block()
            elif pos < len(tokens) and tokens[pos][0] == 'elseif':
                # Treat elseif as else { if ... }
                # Keep 'if' token
                tokens[pos] = ('if', 'if')
                else_body = parse_block()
            if pos < len(tokens) and tokens[pos][0] == 'end':
                pos += 1
            stmts.append(('IF', cond.strip(), then_body, else_body))
        elif t_type == 'CODE':
            stmts.append(('LEAF', t_val))
            pos += 1
        else:
            pos += 1
    return stmts

tree = parse_block()
print(f"Parsed top-level statements: {len(tree)}")

# Now evaluate for each iT in range(0, 120):
def eval_cond(cond_str, iT_val):
    # cond_str is e.g. "not(iT<0X38)" or "iT==86" or "LT[4]==86"
    # If cond_str contains only iT, replace iT with iT_val and evaluate!
    # Convert hex to dec
    s = re.sub(r'0[xX][0-9a-fA-F]+', lambda m: str(int(m.group(0), 16)), cond_str)
    # Check if condition depends on iT
    if 'iT' in s:
        # replace lua ~= with !=
        s_py = s.replace('~=', '!=').replace('iT', str(iT_val))
        try:
            return bool(eval(s_py, {"__builtins__": {}}, {}))
        except Exception:
            return None
    return None # Not an iT condition (e.g. LT[4] == 86)

def trace_op(stmts, iT_val):
    leaves = []
    for stmt in stmts:
        if stmt[0] == 'LEAF':
            leaves.append(stmt[1])
        elif stmt[0] == 'IF':
            _, cond, then_b, else_b = stmt
            res = eval_cond(cond, iT_val)
            if res is True:
                leaves.extend(trace_op(then_b, iT_val))
            elif res is False:
                leaves.extend(trace_op(else_b, iT_val))
            else:
                # Condition depends on runtime operand (e.g. LT[4] == 183)
                leaves.append(f"IF({cond}) -> THEN: {trace_op(then_b, iT_val)} ELSE: {trace_op(else_b, iT_val)}")
    return leaves

op_results = {}
for op in range(0, 120):
    leaves = trace_op(tree, op)
    if leaves:
        clean = " ; ".join(str(x) for x in leaves).replace("\n", " ")
        # condense multiple spaces
        clean = re.sub(r'\s+', ' ', clean)
        op_results[op] = clean

print(f"\nResolved opcodes: {len(op_results)}")
for op in sorted(op_results.keys()):
    print(f"OP {op:3d}: {op_results[op][:140]}")
