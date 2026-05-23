---
sidebar_position: 3
---

# Contributing

`py-sql-cleaner` is an early MVP, so small, focused changes are easiest to review.

## Development Setup

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
```

Run tests:

```bash
.venv/bin/python -m pytest
```

Build the package:

```bash
.venv/bin/python -m build
```

Check built distributions:

```bash
.venv/bin/python -m twine check dist/*
```

## Code Review Tooling

CodeRabbit repository settings live in `.coderabbit.yaml`. Install the CodeRabbit
GitHub App on this public repository to enable automated pull request reviews.

## Guidelines

- Keep changes focused.
- Add or update tests for behavior changes.
- Do not include real production SQL, database hostnames, S3 paths, IAM role
  ARNs, API keys, tokens, passwords, or customer data in tests or fixtures.
- Prefer placeholder values such as `<s3-path>` and `<iam-role-arn>` in examples.
- Keep SQLGlot usage isolated behind the formatter backend.
- Preserve the default safety behavior for f-strings and Jinja-like templates.
