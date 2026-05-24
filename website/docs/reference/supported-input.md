---
sidebar_position: 2
---

# Supported Input

The current MVP targets Python triple-quoted strings.

## Supported

```python
query = """
SELECT *
FROM users
"""
```

```python
load_users_sql = '''
SELECT *
FROM users
'''
```

Detected variable names include:

- `sql`
- `query`
- `*_sql`
- `*_query`

`py-sql-cleaner` also detects SQL-like strings based on keywords such as:

- `SELECT`
- `WITH`
- `INSERT`
- `UPDATE`
- `DELETE`
- `COPY`
- `UNLOAD`
- `QUALIFY`
- `CREATE`
- `MERGE`

Redshift command-style statements such as `COPY` and `UNLOAD` should be run with
`-d redshift`. They are detected and preserved rather than reformatted.

## Not Targeted in the MVP

```python
query = "SELECT * FROM users"
```

Single-line strings, deep Airflow parsing, full f-string handling, and full
Jinja handling are outside the current MVP scope.
