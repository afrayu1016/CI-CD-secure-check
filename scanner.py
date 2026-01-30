#!/usr/bin/env python3
import argparse
import json
import re
import sys
import subprocess
from pathlib import Path

SEVERITY_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3
}

# ---------- Rule Loading ----------

def load_rules(rule_file: str):
    with open(rule_file, "r") as f:
        data = json.load(f)
    return data["rules"]

# ---------- Language Detection ----------

def get_language(path: Path):
    if path.suffix == ".py":
        return "python"
    return None

# ---------- Git Helpers (local mode) ----------

def get_staged_files():
    """
    Return staged files (git add-ed files)
    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True,
        text=True
    )

    files = []
    for line in result.stdout.splitlines():
        path = Path(line)
        if path.exists() and path.suffix == ".py":
            files.append(path)

    return files

# ---------- File Iteration (ci mode) ----------

def iter_python_files(target: Path):
    if target.is_file():
        yield target
    elif target.is_dir():
        yield from target.rglob("*.py")

# ---------- Scanner Core ----------

def scan_file(path: Path, rules):
    findings = []
    lines = path.read_text(errors="ignore").splitlines()

    for lineno, line in enumerate(lines, start=1):
        if "# nosec" in line:
            continue

        for rule in rules:
            if re.search(rule["pattern"], line):
                findings.append({
                    "file": str(path),
                    "line": lineno,
                    "code": line.strip(),
                    "rule": rule
                })

    return findings

# ---------- CLI ----------

def parse_args():
    parser = argparse.ArgumentParser(description="Secure Code Scanner")

    parser.add_argument(
        "--mode",
        choices=["local", "ci"],
        default="ci",
        help="Execution mode (local = staged files, ci = repository scan)"
    )

    parser.add_argument(
        "--rules",
        required=True,
        help="Path to rules.json"
    )

    parser.add_argument(
        "--fail-level",
        choices=SEVERITY_ORDER.keys(),
        default="HIGH",
        help="Minimum severity level to fail"
    )

    parser.add_argument(
        "targets",
        nargs="*",
        default=["."],
        help="Files or directories to scan (used in ci mode)"
    )

    return parser.parse_args()

# ---------- Main ----------

def main():
    args = parse_args()
    rules = load_rules(args.rules)
    fail_threshold = SEVERITY_ORDER[args.fail_level]

    blocked = False

    if args.mode == "local":
        print("🔍 Mode: local (staged files)")
        targets = get_staged_files()

        if not targets:
            print("ℹ️ No staged Python files to scan.")
            sys.exit(0)

    else:
        print("🔍 Mode: ci (repository scan)")
        targets = []
        for t in args.targets:
            targets.append(Path(t))

    for target in targets:
        if args.mode == "ci":
            files = iter_python_files(target)
        else:
            files = [target]

        for file_path in files:
            lang = get_language(file_path)
            if not lang:
                continue

            applicable_rules = [
                r for r in rules if r["language"] == lang
            ]

            findings = scan_file(file_path, applicable_rules)

            for f in findings:
                rule = f["rule"]
                severity = rule["severity"]

                print(
                    f"❌ {f['file']}:{f['line']} "
                    f"[{rule['id']} | {severity}]\n"
                    f"    {rule['message']}\n"
                    f"    > {f['code']}\n"
                )

                if SEVERITY_ORDER[severity] >= fail_threshold:
                    blocked = True

    if blocked:
        print("❌ Security issues detected")
        sys.exit(1)
    else:
        print("✅ No security issues found")
        sys.exit(0)

if __name__ == "__main__":
    main()
