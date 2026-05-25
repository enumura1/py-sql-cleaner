---
sidebar_position: 1
---

# Introduction

`py-sql-cleaner` is a CLI tool for finding, formatting, and extracting SQL
embedded in Python files.

It is built for codebases where long SQL queries are written directly inside
triple-quoted Python strings. The current MVP uses SQLGlot for formatting,
defaults to SQLGlot's generic dialect, and can format with database-specific
dialects that this project has explicitly enabled via `--dialect`.

```python
query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
```

`py-sql-cleaner` can format that SQL in place, or extract it into an external `.sql`
file.

:::note
`py-sql-cleaner` is an early MVP. It uses SQLGlot internally for best-effort SQL
formatting. It does not connect to databases and does not execute SQL.
Dialect support means SQLGlot parser/formatter mode selection, not exhaustive
database validation. Redshift command-style statements such as `COPY` and
`UNLOAD` are preserved rather than reformatted to avoid changing load/export
options.
:::

## What It Helps With

- Making Python files easier to read when they contain long SQL strings
- Moving embedded SQL into `.sql` files for review and reuse
- Checking formatting in CI
- Avoiding risky rewrites of f-strings, Jinja-like templates, and runtime
  placeholders

## Current Scope

- Python files
- triple-quoted SQL strings
- SQLGlot-backed SQL formatting, defaulting to generic SQL with `--dialect`
  support for explicitly enabled database-specific formatting
- formatting
- extracting SQL into `.sql` files
