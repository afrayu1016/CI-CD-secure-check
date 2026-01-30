A lightweight Python-based Static Application Security Testing (SAST) tool that scans source code for common insecure coding patterns using configurable JSON rules.
Designed to integrate seamlessly with Git pre-commit hooks and GitHub Actions for automated security enforcement.

### Features
1. Regex-based static code scanning
2. Rules defined in JSON (easy to extend)
3. Severity-based enforcement (HIGH / MEDIUM / LOW)
4. Git pre-commit hook support
5. GitHub Actions CI integration
6. Test cases for quick validation

### Project Structure
.
├── scanner.py              # Core scanning engine
├── rules.json              # Security rules definition
├── hash.py                 # Hash utulity for Secure test cases (for demo)
├── ci_fail.py                 # Insecure test cases (for demo)
├── .github/
│   └── workflows/
│       └── secure-scan.yml # GitHub Actions workflow
└── README.md

### Usage: Single file scan
python scanner.py test.py
