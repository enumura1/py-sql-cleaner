# Contributing

Thanks for your interest in contributing to `py-sql-cleaner`.

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

Run lint checks:

```bash
.venv/bin/python -m ruff check .
```

Build the package:

```bash
.venv/bin/python -m build
```

Check built distributions:

```bash
.venv/bin/python -m twine check dist/*
```

## Contribution Guidelines

- Keep changes focused.
- Add or update tests for behavior changes.
- Do not include real production SQL, database hostnames, S3 paths, IAM role
  ARNs, API keys, tokens, passwords, or customer data in tests or fixtures.
- Prefer placeholder values such as `<s3-path>` and `<iam-role-arn>` in examples.
- Keep SQLGlot usage isolated behind the formatter backend.
- Preserve the default safety behavior for f-strings and Jinja-like templates.

## Scope

The current focus is:

- Python files
- triple-quoted SQL strings
- SQLGlot-backed SQL formatting, currently defaulting to the Redshift dialect
- formatting
- extracting SQL into `.sql` files

Please open an issue before starting large features such as new dialect support,
template handling, or formatter backend changes.
