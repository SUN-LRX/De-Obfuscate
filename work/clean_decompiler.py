import re
from pathlib import Path
from collections import defaultdict

# Load Proto 0
raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0 = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0[pc][field] = val

OP_NAMES = {
    0: "TFORLOOP", 1: "NOT", 2: "CLOSURE", 3: "GETGLOBAL", 4: "EQ_CONST", 5: "BAND",
    6: "POW_CONST", 7: "JUMP_IF_NE", 8: "SETLIST", 9: "TFORCALL", 10: "SETTABLE_FIELD",
    11: "JUMP_IF_LT", 12: "GE_CONST", 13: "IDIV", 14: "SETUPVAL", 15: "CONCAT",
    16: "BOR", 17: "LOADBOOL_TRUE", 18: "SETUPVAL", 19: "CALL1", 20: "JUMP_IF_LT",
    21: "JUMP_IF_EQ_CONST", 22: "SUB_CONST", 23: "LOADK", 24: "JUMP_IF_NOT_LE_CONST",
    25: "GETUPVAL", 26: "SELF_MODIFY", 27: "CLOSE", 28: "JUMP_IF_LT_REV", 29: "MOD_CONST",
    30: "RETURN", 31: "MOD", 32: "VARARG", 33: "JUMP_IF_TRUE", 34: "BXOR",
    35: "FORPREP", 36: "DIV", 37: "EQ", 38: "LOADNIL", 39: "TFORCALL",
    40: "JUMP_IF_LT_CONST", 41: "LEN", 42: "CALL0", 43: "SUB_REV_CONST", 44: "GETENV",
    45: "CALL2_VOID", 46: "JUMP_IF_EQ_CONST", 47: "JUMP_IF_EQ", 48: "SELF",
    49: "LE", 50: "CALL_VARARGS", 51: "CALL_MULTRET", 52: "NE_CONST", 53: "TFORLOOP",
    54: "SETLIST", 55: "JUMP_IF_LE", 56: "FORLOOP", 57: "JUMP_IF_GT", 58: "RSHIFT",
    59: "SELF_MODIFY", 60: "CALL_VARARGS_1RET", 61: "LOADBOOL_FALSE", 62: "POW",
    63: "MUL", 64: "JUMP_IF_LT", 65: "LT", 66: "SETUPVAL", 67: "BNOT",
    68: "CLOSE", 69: "MOVE", 70: "RETURN", 71: "POW_REV_CONST", 72: "SETLIST",
    73: "LOADNIL", 74: "JUMP", 75: "MOVE", 76: "CALL2", 77: "MUL_CONST",
    78: "GE", 79: "GT", 80: "CALL_VARARGS_VOID", 81: "UNM", 82: "VARARG",
    83: "ADD_CONST", 84: "JUMP_IF_FALSE", 85: "ADD", 86: "GETTABLE", 87: "CALL",
    88: "SETGLOBAL", 89: "CONCAT", 90: "CALL1_VOID", 91: "RETURN", 92: "DIV_CONST",
    93: "SETTABLE_CONST", 94: "LSHIFT", 95: "MUL_CONST", 96: "VARARG", 97: "NEWTABLE",
    98: "CALL0", 99: "SETTABLE", 100: "RETURN_FALSE", 101: "NE", 102: "LOADK",
    103: "GETUPVAL", 104: "RETURN", 105: "FORLOOP", 106: "TFORCALL", 107: "FORLOOP_STEP",
    108: "DIV_CONST", 109: "SUB", 110: "GETTABLE_CONST", 111: "SETTABLE",
}

def resolve_jump(target_pc):
    # Follow jump chains (jump threading)
    visited = set()
    curr = target_pc
    while curr in proto0 and curr not in visited:
        visited.add(curr)
        op = int(proto0[curr].get(3, -1))
        if op == 74: # JUMP
            f5 = proto0[curr].get(5)
            if f5 and f5.isdigit():
                curr = int(f5)
            else:
                break
        else:
            break
    return curr

# High-level decompiler:
regs = {}
lines = []

def expr(r):
    return regs.get(r, f"r{r}")

# Follow execution from PC 1
curr = 1
visited = set()

while curr and curr in proto0 and curr not in visited:
    visited.add(curr)
    row = proto0[curr]
    f3 = int(row.get(3, -1)) if row.get(3, '').lstrip('-').isdigit() else -1
    op = OP_NAMES.get(f3, f"OP_{f3}")
    f1 = row.get(1, '')
    f2 = int(row.get(2, 0)) if row.get(2, '').lstrip('-').isdigit() else 0
    f4 = int(row.get(4, 0)) if row.get(4, '').lstrip('-').isdigit() else 0
    f5 = int(row.get(5, 0)) if row.get(5, '').lstrip('-').isdigit() else 0
    f6 = row.get(6, '')

    if op == "JUMP":
        curr = resolve_jump(f5)
        continue
    elif op == "GETGLOBAL":
        gname = "game" if f6 == "-3624381080" else ("task" if f5 == 460 else f"_ENV[{f5}]")
        regs[f2] = gname
    elif op == "LOADK":
        regs[f2] = repr(f6) if f6 and f6 not in ('10', '12') else repr(f5)
    elif op == "LOADNIL":
        regs[f2] = "nil"
    elif op == "LOADBOOL_TRUE":
        regs[f2] = "true"
    elif op == "LOADBOOL_FALSE":
        regs[f2] = "false"
    elif op == "NEWTABLE":
        regs[f2] = "{}"
    elif op == "MOVE":
        regs[f2] = expr(f5)
    elif op == "GETTABLE":
        regs[f2] = f"{expr(f5)}[{expr(f4)}]"
    elif op == "GETTABLE_CONST":
        regs[f2] = f"{expr(f5)}[{repr(f4)}]"
    elif op == "SETTABLE":
        lines.append(f"{expr(f2)}[{expr(f5)}] = {expr(f4)}")
    elif op == "SETTABLE_CONST":
        lines.append(f"{expr(f2)}[{repr(f4)}] = {repr(f5)}")
    elif op == "SETTABLE_FIELD":
        lines.append(f"{expr(f2)}[{repr(f4)}] = {expr(f5)}")
    elif op == "SELF":
        obj = expr(f5)
        method_name = "GetService" if f4 == 188 else f"method_{f4}"
        regs[f2 + 1] = obj
        regs[f2] = f"{obj}:{method_name}"
    elif op == "CALL0":
        lines.append(f"{expr(f2)}()")
    elif op == "CALL1":
        fn = expr(f2)
        arg = expr(f2 + 1)
        lines.append(f"{fn}({arg})")
    elif op == "CALL2":
        fn = expr(f2)
        a1 = expr(f2 + 1)
        a2 = expr(f2 + 2)
        lines.append(f"{fn}({a1}, {a2})")
    elif op in ("CALL", "CALL_MULTRET"):
        lines.append(f"{expr(f2)}(...)")
    elif op == "CLOSURE":
        regs[f2] = f"function_proto_{f5}"
    elif op == "RETURN":
        lines.append(f"return {expr(f2)}")
        break
    elif op == "JUMP_IF_TRUE":
        lines.append(f"if {expr(f2)} then")
        curr = resolve_jump(f5)
        continue
    elif op == "JUMP_IF_FALSE":
        lines.append(f"if not ({expr(f2)}) then")
        curr = resolve_jump(f5)
        continue

    curr = resolve_jump(curr + 1)

print("--- RECONSTRUCTED CLEAN HIGH-LEVEL SCRIPT ---")
for l in lines:
    print(l)
