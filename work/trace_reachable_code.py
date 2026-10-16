import re
from pathlib import Path
from collections import defaultdict, deque

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0_insts = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_insts[pc][field] = val

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

# Linearize reachable instructions by following control flow:
visited = set()
curr = 1
trace = []

while curr and curr in proto0_insts and curr not in visited:
    visited.add(curr)
    row = proto0_insts[curr]
    f3 = int(row.get(3, -1)) if row.get(3, '').lstrip('-').isdigit() else -1
    op_name = OP_NAMES.get(f3, f"OP_{f3}")
    f1 = row.get(1, '')
    f2 = row.get(2, '')
    f4 = row.get(4, '')
    f5 = row.get(5, '')
    f6 = row.get(6, '')
    trace.append((curr, op_name, f1, f2, f4, f5, f6))
    
    if op_name == "JUMP":
        curr = int(f5) if f5.isdigit() else None
    elif op_name in ("JUMP_IF_FALSE", "JUMP_IF_TRUE"):
        # For tracing, follow the jump target or fallthrough
        target = int(f5) if f5.isdigit() else None
        curr = target
    elif "RETURN" in op_name:
        break
    else:
        curr = curr + 1

print(f"Traced path length: {len(trace)}")
for pc, op, f1, f2, f4, f5, f6 in trace:
    if op != "JUMP":
        print(f"PC {pc:4d}: {op:<16} r{f2}, f4={f4}, f5={f5}, f6={f6}, f1={f1}")
    else:
        print(f"PC {pc:4d}: JUMP -> {f5}")
