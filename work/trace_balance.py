import re

def trace_balance(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stack = []
    for line_no, line in enumerate(lines, 1):
        clean = line.split('--')[0]
        clean = re.sub(r'"(\\.|[^"])*"', '""', clean)
        clean = re.sub(r"'(\\.|[^'])*'", "''", clean)
        tokens = re.findall(r'\b(function|then|do|repeat|end|until)\b', clean)
        for t in tokens:
            if t in ['function', 'then', 'do', 'repeat']:
                stack.append((t, line_no, line.strip()))
            elif t in ['end', 'until']:
                if stack:
                    stack.pop()
                else:
                    print(f"Extra end at line {line_no}: {line.strip()}")
    print(f"Unclosed in {filepath}:")
    for item in stack:
        print(f"  Line {item[1]}: {item[0]} -> {item[2]}")

trace_balance('outputs/modules/04_ui_library.lua')
trace_balance('outputs/hohohub_master_complete.lua')
