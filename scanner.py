import json
import re
import sys
import argparse
from pathlib import Path

RULE_FILE = "rule.json"
SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

def load_rules():
    with open(RULE_FILE, "r") as f:
        data = json.load(f)
    return data["rules"]

def get_language(file_path):
    if file_path.endswith(".py"):
        return "python"
    return None

def parse_args():
    parser = argparse.ArgumentParser(description="Secure Code Scanner")
    parser.add_argument(
        "files",
        nargs="+",
        help="Files to scan"
    )
    parser.add_argument(
        "--fail-level",
        default="HIGH",
        choices=SEVERITY_ORDER.keys(),
        help="Minimum severity level to fail"
    )
    return parser.parse_args()

def scan_file(path, rules, fail_level):
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

def main():
    args = parse_args()
    rules = load_rules()
    fail_threshold = SEVERITY_ORDER[args.fail_level]

    blocked = False

    for file in args.files:
        lang = get_language(file)
        if not lang:
            continue

        applicable_rules = [r for r in rules if r["language"] == lang]
        findings = scan_file(Path(file), applicable_rules, fail_threshold)

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
        print("🚫 Commit/CI blocked due to security policy.")
        sys.exit(1)

    print("✅ Security scan passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
