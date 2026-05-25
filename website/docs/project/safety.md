---
sidebar_position: 1
---

# Safety and Limitations

`py-sql-cleaner` is conservative by default. It skips unsafe blocks instead of
rewriting them.

:::note
Skipped blocks are left unchanged. Preserving runtime behavior is more important
than formatting every SQL-looking string.
:::

## Unsafe Blocks

f-strings are always skipped by `format` and `extract`:

```python
query = f"""
SELECT *
FROM users
WHERE user_id = {user_id}
"""
```

Jinja-like templates are also always skipped by `format` and `extract`:

```python
query = """
SELECT *
FROM users
WHERE ds = '{{ ds }}'
"""
```

Runtime placeholders are also always skipped by `format` and `extract`:

```python
query = """
SELECT *
FROM users
WHERE user_id = :user_id
"""
```

```python
query = """
SELECT *
FROM users
WHERE user_id = %s
"""
```

Reasons:

- f-strings may contain Python expressions
- Jinja-like templates may be used by Airflow, dbt, or other tools
- placeholders such as `:user_id`, `%s`, and `%(user_id)s` are filled by a
  database driver or query builder
- these strings are completed at runtime, after Python, a template engine, a
  database driver, or a query builder fills in values
- rewriting these strings incorrectly could change runtime behavior

## What py-sql-cleaner Does Not Do

`py-sql-cleaner` does not:

- connect to databases
- execute SQL
- validate SQL against a database
- inspect schemas
- provide autocomplete
- guarantee full database compatibility
- fully support f-strings
- fully support Jinja templates
- rewrite parameterized SQL safely
- format every possible SQL string
