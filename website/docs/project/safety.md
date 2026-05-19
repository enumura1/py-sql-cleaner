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

f-strings are skipped by default:

```python
query = f"""
SELECT *
FROM users
WHERE user_id = {user_id}
"""
```

Jinja-like templates are also skipped during formatting:

```python
query = """
SELECT *
FROM users
WHERE ds = '{{ ds }}'
"""
```

Reasons:

- f-strings may contain Python expressions
- Jinja-like templates may be used by Airflow, dbt, or other tools
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
- format every possible SQL string
