import re
import glob

def check_lua(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    # Remove block comments --[[ ... ]]
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    # Remove single line comments
    code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
    # Remove string literals
    code = re.sub(r'"(\\.|[^"])*"', '""', code)
    code = re.sub(r"'(\\.|[^'])*'", "''", code)
    # Replace elseif ... then so that 'then' is not double-counted for the single 'end'
    code = re.sub(r'\belseif\b[^\n]*?\bthen\b', '', code)

    tokens = re.findall(r'\b(function|then|do|repeat|end|until)\b', code)
    balance = sum(1 if t in ['function', 'then', 'do', 'repeat'] else -1 for t in tokens)
    print(f"{filepath}: balance = {balance}")

for f in glob.glob('outputs/**/*.lua', recursive=True):
    check_lua(f)
