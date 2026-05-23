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

Run the full local harness:

```bash
scripts/check
```

Run individual lint checks:

```bash
.venv/bin/python -m ruff format --check .
.venv/bin/python -m ruff check .
.venv/bin/lint-imports
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
- Use the branching strategy in `docs/development/branching.md`; do not push
  directly to `main`.
- Add or update tests for behavior changes.
- Keep package dependencies flowing in the direction documented in
  `docs/architecture/README.md`.
- Do not include real production SQL, database hostnames, S3 paths, IAM role
  ARNs, API keys, tokens, passwords, or customer data in tests or fixtures.
- Prefer placeholder values such as `<s3-path>` and `<iam-role-arn>` in examples.
- Keep SQLGlot usage isolated behind the formatter backend.
- Preserve the default safety behavior for f-strings and Jinja-like templates.

## Pre-push Hook

Enable the repository hook once:

```bash
git config core.hooksPath .githooks
```

The pre-push hook runs `scripts/check`, matching the local harness and CI.

## Code Review Tooling

CodeRabbit repository settings live in `.coderabbit.yaml`. Install the CodeRabbit
GitHub App on this public repository to enable automated pull request reviews.

## Scope

The current focus is:

- Python files
- triple-quoted SQL strings
- SQLGlot-backed SQL formatting, defaulting to generic SQL with `--dialect`
  support for database-specific formatting
- formatting
- extracting SQL into `.sql` files

Please open an issue before starting large features such as template handling,
formatter backend changes, or support that goes beyond SQLGlot dialect selection.
