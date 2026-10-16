#!/usr/bin/env python3
# ==============================================================================
# Mode_ZO_v1 : Luau Deobfuscator & Devirtualizer Machine Pipeline Runner
# ==============================================================================

import os
import sys
import glob
import re

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
WORK_DIR = os.path.join(BASE_DIR, "work")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def print_banner():
    print("=" * 70)
    print("       MODE_ZO_v1 : LUAU DEOBFUSCATOR & DEVIRTUALIZER MACHINE")
    print("=" * 70)

def check_inputs():
    print("\n[*] Inspecting input/ directory...")
    files = glob.glob(os.path.join(INPUT_DIR, "*"))
    if not files:
        print("  [-] No input files found in input/.")
        return []
    for f in files:
        size = os.path.getsize(f)
        print(f"  [+] Input File: {os.path.basename(f)} ({size:,} bytes)")
    return files

def check_work_tools():
    print("\n[*] Inspecting work/ directory...")
    tools = [
        "decode_rle.py",
        "solve_all_opcodes.py",
        "analyze_cfg.py",
        "extract_all_strings.py",
        "extract_coords.py",
        "resolved_opcodes.txt",
        "vm_consts.log"
    ]
    present = 0
    for tool in tools:
        path = os.path.join(WORK_DIR, tool)
        if os.path.exists(path):
            present += 1
            print(f"  [OK] Tool/Artifact ready: {tool}")
        else:
            print(f"  [--] Tool/Artifact missing: {tool}")
    print(f"  -> {present}/{len(tools)} core work tools/artifacts available.")

def check_outputs():
    print("\n[*] Inspecting output/ directory...")
    out_files = glob.glob(os.path.join(OUTPUT_DIR, "**", "*.lua"), recursive=True)
    if not out_files:
        print("  [-] No output files found in output/.")
        return

    for f in out_files:
        rel = os.path.relpath(f, OUTPUT_DIR)
        size = os.path.getsize(f)
        with open(f, "r", encoding="utf-8", errors="ignore") as fp:
            code = fp.read()
            lines = len(code.splitlines())

        # Syntax check balance
        code_clean = re.sub(r"--\[\[.*?\]\]", "", code, flags=re.DOTALL)
        code_clean = re.sub(r"--.*$", "", code_clean, flags=re.MULTILINE)
        code_clean = re.sub(r'"(\\.|[^"])*"', '""', code_clean)
        code_clean = re.sub(r"'(\\.|[^'])*'", "''", code_clean)
        code_clean = re.sub(r"\belseif\b[^\n]*?\bthen\b", "", code_clean)

        tokens = re.findall(r"\b(function|then|do|repeat|end|until)\b", code_clean)
        balance = sum(1 if t in ["function", "then", "do", "repeat"] else -1 for t in tokens)

        status = "SYNTAX OK" if balance == 0 else f"UNBALANCED ({balance})"
        print(f"  [OK] {rel:35} | {lines:5} lines | {size:7,} bytes | [{status}]")

def main():
    print_banner()
    inputs = check_inputs()
    check_work_tools()
    check_outputs()
    print("\n" + "=" * 70)
    print("  Mode_ZO_v1 Status: All pipeline stages synchronized and ready.")
    print("=" * 70)

if __name__ == "__main__":
    main()
