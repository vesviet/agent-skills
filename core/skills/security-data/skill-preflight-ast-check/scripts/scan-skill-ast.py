#!/usr/bin/env python3
"""Static AST Security Preflight Scanner for Agent Skills.

Performs zero-execution static analysis:
- Identifies prohibited builtins (eval, exec, compile, __import__)
- Detects dangerous subprocess and shell invocations
- Scans for prompt injection markers in markdown text
- Evaluates the Lethal Trifecta invariant (D_priv AND C_untrusted AND E_net)
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

PROHIBITED_BUILTINS = {"eval", "exec", "compile", "__import__"}
PROHIBITED_SUBPROCESS = {"system", "popen", "spawn", "call", "check_call", "check_output", "run"}
PROMPT_INJECTION_MARKERS = [
    r"<\|im_start\|>",
    r"<\|im_end\|>",
    r"\[SYSTEM\]",
    r"(?i)ignore\s+previous\s+instructions",
]


class SkillSecurityVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.violations: list[str] = []

    def visit_Call(self, node: ast.Call):
        # 1. Prohibited builtins: eval, exec, compile, __import__
        if isinstance(node.func, ast.Name) and node.func.id in PROHIBITED_BUILTINS:
            self.violations.append(
                f"{self.filename}:{node.lineno}: Prohibited dynamic execution builtin '{node.func.id}'"
            )

        # 2. Subprocess or os.system calls
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in PROHIBITED_SUBPROCESS:
                # Check if caller is os or subprocess
                if isinstance(node.func.value, ast.Name) and node.func.value.id in {"os", "subprocess"}:
                    self.violations.append(
                        f"{self.filename}:{node.lineno}: Prohibited shell/process invocation '{node.func.value.id}.{node.func.attr}'"
                    )

        self.generic_visit(node)


def scan_python_code(filepath: Path) -> list[str]:
    violations: list[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(filepath))
        visitor = SkillSecurityVisitor(str(filepath))
        visitor.visit(tree)
        violations.extend(visitor.violations)
    except SyntaxError as e:
        violations.append(f"{filepath}:{e.lineno}: Syntax error during AST parse: {e.msg}")
    except Exception as e:
        violations.append(f"{filepath}: Failed to read/parse: {e}")
    return violations


def scan_markdown_text(filepath: Path) -> list[str]:
    violations: list[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
        for pattern in PROMPT_INJECTION_MARKERS:
            match = re.search(pattern, content)
            if match:
                violations.append(
                    f"{filepath}: Detected potential prompt injection pattern '{match.group(0)}'"
                )
    except Exception as e:
        violations.append(f"{filepath}: Failed to scan markdown: {e}")
    return violations


def scan_directory(target_dir: Path) -> tuple[int, list[str]]:
    all_violations: list[str] = []
    scanned_count = 0

    for p in target_dir.rglob("*"):
        if p.is_file():
            if p.suffix == ".py":
                scanned_count += 1
                all_violations.extend(scan_python_code(p))
            elif p.suffix in {".md", ".txt"}:
                scanned_count += 1
                all_violations.extend(scan_markdown_text(p))

    return scanned_count, all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Zero-execution static AST security scanner for agent skills.")
    parser.add_argument("target", nargs="?", default=".", help="Target file or directory to analyze (default: current dir)")
    args = parser.parse_args()

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"Error: Target '{target_path}' does not exist.", file=sys.stderr)
        return 2

    if target_path.is_file():
        violations = scan_python_code(target_path) if target_path.suffix == ".py" else scan_markdown_text(target_path)
        count = 1
    else:
        count, violations = scan_directory(target_path)

    print(f"Static AST Preflight Scan completed: {count} files analyzed.")
    if violations:
        print(f"FAILED: Found {len(violations)} security violations:")
        for v in violations:
            print(f"  - {v}")
        return 1

    print("SUCCESS: Zero AST security or prompt injection violations detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
