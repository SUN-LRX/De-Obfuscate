import re
from pathlib import Path
from collections import defaultdict

# 1. Opcode dictionary
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

# 2. Parse Proto 0
raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0_insts = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_insts[pc][field] = val

# Decompiler simulation:
regs = {}
code_output = []
jump_targets = set()

# Find all jump targets
for pc, row in proto0_insts.items():
    f3 = int(row.get(3, -1)) if row.get(3, '').lstrip('-').isdigit() else -1
    op_name = OP_NAMES.get(f3, '')
    if "JUMP" in op_name:
        tgt = row.get(5) if op_name == "JUMP" or "FALSE" in op_name or "TRUE" in op_name else row.get(2)
        if tgt and tgt.isdigit():
            jump_targets.add(int(tgt))

def get_reg(r):
    return regs.get(r, f"r{r}")

for pc in sorted(proto0_insts.keys()):
    if pc in jump_targets:
        code_output.append(f"\n::L_{pc}::")
    row = proto0_insts[pc]
    f1 = row.get(1, '')
    f2 = int(row.get(2, 0)) if row.get(2, '').lstrip('-').isdigit() else 0
    f3 = int(row.get(3, -1)) if row.get(3, '').lstrip('-').isdigit() else -1
    f4 = row.get(4, '')
    f5 = row.get(5, '')
    f6 = row.get(6, '')
    op_name = OP_NAMES.get(f3, f"OP_{f3}")

    f4_int = int(f4) if f4.lstrip('-').isdigit() else 0
    f5_int = int(f5) if f5.lstrip('-').isdigit() else 0

    if op_name == "JUMP":
        code_output.append(f"goto L_{f5};")
    elif op_name == "JUMP_IF_FALSE":
        code_output.append(f"if not ({get_reg(f2)}) then goto L_{f5}; end")
    elif op_name == "JUMP_IF_TRUE":
        code_output.append(f"if ({get_reg(f2)}) then goto L_{f5}; end")
    elif op_name == "JUMP_IF_EQ":
        code_output.append(f"if ({get_reg(f5_int)} == {get_reg(f4_int)}) then goto L_{f2}; end")
    elif op_name == "JUMP_IF_NE":
        code_output.append(f"if ({get_reg(f5_int)} ~= {get_reg(f4_int)}) then goto L_{f2}; end")
    elif op_name == "JUMP_IF_LT":
        code_output.append(f"if ({get_reg(f5_int)} < {get_reg(f4_int)}) then goto L_{f2}; end")
    elif op_name == "JUMP_IF_LE":
        code_output.append(f"if ({get_reg(f5_int)} <= {get_reg(f4_int)}) then goto L_{f2}; end")
    elif op_name == "GETGLOBAL":
        gname = "game" if f6 == "-3624381080" else f"_ENV[{f6}]"
        regs[f2] = gname
    elif op_name == "SETGLOBAL":
        gname = "game" if f6 == "-3624381080" else f"_ENV[{f6}]"
        code_output.append(f"{gname} = {get_reg(f2)};")
    elif op_name == "GETTABLE":
        regs[f2] = f"{get_reg(f5_int)}[{get_reg(f4_int)}]"
    elif op_name == "GETTABLE_CONST":
        key = f1 if f1 else f4
        regs[f2] = f"{get_reg(f5_int)}[{repr(key)}]"
    elif op_name == "SETTABLE":
        val = get_reg(f4_int) if f4 else f1
        code_output.append(f"{get_reg(f2)}[{get_reg(f5_int)}] = {val};")
    elif op_name == "SETTABLE_CONST":
        code_output.append(f"{get_reg(f2)}[{repr(f6)}] = {repr(f1)};")
    elif op_name == "SETTABLE_FIELD":
        code_output.append(f"{get_reg(f2)}[{repr(f6)}] = {get_reg(f5_int)};")
    elif op_name == "MOVE":
        regs[f2] = get_reg(f5_int)
    elif op_name == "LOADK":
        val = f6 if f6 and f6 != '10' else (f1 if f1 else f5)
        regs[f2] = str(val)
    elif op_name == "LOADNIL":
        regs[f2] = "nil"
    elif op_name == "LOADBOOL_TRUE":
        regs[f2] = "true"
    elif op_name == "LOADBOOL_FALSE":
        regs[f2] = "false"
    elif op_name == "CLOSURE":
        regs[f2] = f"closure_proto_{f5}"
    elif op_name == "CALL0":
        fn = get_reg(f2)
        code_output.append(f"{fn}();")
    elif op_name == "CALL1":
        fn = get_reg(f2)
        arg = get_reg(f2 + 1)
        code_output.append(f"{fn}({arg});")
    elif op_name == "CALL2":
        fn = get_reg(f2)
        a1 = get_reg(f2 + 1)
        a2 = get_reg(f2 + 2)
        code_output.append(f"{fn}({a1}, {a2});")
    elif op_name in ("CALL", "CALL_VARARGS", "CALL_MULTRET"):
        fn = get_reg(f2)
        code_output.append(f"{fn}(...);")
    elif op_name == "SELF":
        obj = get_reg(f5_int)
        regs[f2 + 1] = obj
        regs[f2] = f"{obj}:{f4}"
    elif op_name == "ADD":
        regs[f2] = f"({get_reg(f5_int)} + {get_reg(f4_int)})"
    elif op_name == "SUB":
        regs[f2] = f"({get_reg(f5_int)} - {get_reg(f4_int)})"
    elif op_name == "MUL":
        regs[f2] = f"({get_reg(f5_int)} * {get_reg(f4_int)})"
    elif op_name == "DIV":
        regs[f2] = f"({get_reg(f5_int)} / {get_reg(f4_int)})"
    elif op_name == "MOD":
        regs[f2] = f"({get_reg(f5_int)} % {get_reg(f4_int)})"
    elif op_name == "CONCAT":
        regs[f2] = f"({get_reg(f5_int)} .. {get_reg(f4_int)})"
    elif op_name == "RETURN":
        code_output.append(f"return {get_reg(f2)};")
    elif op_name == "NEWTABLE":
        regs[f2] = "{}"
    else:
        code_output.append(f"-- {op_name} r{f2}")

decompiled_script = "\n".join(code_output)
with open("work/proto0_decompiled.lua", "w", encoding="utf-8") as f:
    f.write(decompiled_script)

print(f"Decompiled script saved to work/proto0_decompiled.lua ({len(code_output)} lines)")
print("\nFirst 60 lines of decompiled script:")
print("\n".join(code_output[:60]))
