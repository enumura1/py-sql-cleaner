---
sidebar_position: 1
---

# Introduction

`pyredsql` is a Redshift-first CLI tool for formatting and extracting SQL
embedded in Python files.

It is built for codebases where long Redshift SQL queries are written directly
inside triple-quoted Python strings:

```python
query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
```

`pyredsql` can format that SQL in place, or extract it into an external `.sql`
file.

:::note
`pyredsql` is an early MVP. It uses SQLGlot internally for best-effort SQL
formatting. It does not connect to databases and does not execute SQL.
:::

## What It Helps With

- Making Python files easier to read when they contain long SQL strings
- Moving embedded SQL into `.sql` files for review and reuse
- Checking formatting in CI
- Avoiding risky rewrites of f-strings and Jinja-like templates

## Current Scope

- Python files
- triple-quoted SQL strings
- Redshift SQL
- formatting
- extracting SQL into `.sql` files
