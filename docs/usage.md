# Usage Guide

This guide shows the main `pyredsql` workflows.

## List Embedded SQL Blocks

```bash
pyredsql list jobs/load_users.py
```

Example output:

```text
Found 1 SQL blocks

1. jobs/load_users.py:3-7
   variable: query
   confidence: 0.95
   unsafe: false
```

## Format Embedded SQL

```bash
pyredsql format jobs/load_users.py
```

Preview changes first:

```bash
pyredsql format jobs/load_users.py --dry-run
```

Check formatting without modifying files:

```bash
pyredsql check jobs/load_users.py
```

If embedded SQL is not formatted, `pyredsql check` exits with a non-zero status
code.

## Extract Embedded SQL

```bash
pyredsql extract jobs/load_users.py --out-dir sql
```

By default, `extract` replaces the embedded SQL with a path string:

```python
query = "sql/query.sql"
```

Use `read-text` replacement mode:

```bash
pyredsql extract jobs/load_users.py --out-dir sql --replace-mode read-text
```

Result:

```python
query = Path("sql/query.sql").read_text()
```

Note: `pyredsql` does not automatically insert `from pathlib import Path` in the
current MVP.

Specify an output name:

```bash
pyredsql extract jobs/load_users.py --out-dir sql --name load_users
```

## Example Workflow

```bash
pyredsql list jobs/load_users.py
pyredsql format jobs/load_users.py --dry-run
pyredsql format jobs/load_users.py
pyredsql extract jobs/load_users.py --out-dir sql
```

Then review the diff:

```bash
git diff
```
