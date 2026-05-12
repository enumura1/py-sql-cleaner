---
sidebar_position: 2
---

# Quick Start

## 1. List Embedded SQL Blocks

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

## 2. Preview Formatting Changes

```bash
pyredsql format jobs/load_users.py --dry-run
```

## 3. Format Embedded SQL

```bash
pyredsql format jobs/load_users.py
```

Before:

```python
query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
```

After:

```python
query = """
SELECT
  user_id,
  updated_at
FROM users
QUALIFY
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY updated_at DESC) = 1
"""
```

Exact formatting is produced by SQLGlot and may change as SQLGlot changes.

## 4. Extract SQL

```bash
pyredsql extract jobs/load_users.py --out-dir sql
```

After extraction:

```python
query = "sql/query.sql"
```

## 5. Check Formatting in CI

```bash
pyredsql check jobs/load_users.py
```

If embedded SQL is not formatted, `pyredsql check` exits with a non-zero status
code.
