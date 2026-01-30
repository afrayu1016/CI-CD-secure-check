# Automated Secure Coding Assistant

A lightweight **Python-based Static Application Security Testing (SAST)** tool that scans source code for common insecure coding patterns using configurable JSON rules.  
Designed to integrate seamlessly with **Git pre-commit hooks** and **GitHub Actions** for automated security enforcement.

---

## Features

- Regex-based static code scanning
- Rules defined in JSON (easy to extend)
- Severity-based enforcement (**HIGH / MEDIUM / LOW**)
- Git pre-commit hook support
- GitHub Actions CI integration
- Test cases for quick validation

---

## Project Structure

```text
.
├── scanner.py              # Core scanning engine
├── rules.json              # Security rules definition
├── hash.py                 # Hash utility for secure test cases (demo)
├── ci_fail.py              # Insecure test cases (demo)
├── .github/
│   └── workflows/
│       └── secure-scan.yml # GitHub Actions workflow
└── README.md
