# Safety and Limitations

`pyredsql` is conservative by default. It prefers skipping blocks over rewriting
SQL that may contain runtime logic.

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

## Supported Input

The current MVP targets Python triple-quoted strings:

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

Single-line strings are not targeted in the MVP:

```python
query = "SELECT * FROM users"
```

## Redshift-First

`pyredsql` is designed primarily for Amazon Redshift SQL.

Formatting is powered by SQLGlot internally. `pyredsql` does not aim to be a
full SQL parser or a replacement for SQLGlot. Its main responsibility is to find
SQL embedded in Python files and refactor it safely.

## What pyredsql Does Not Do

`pyredsql` does not:

- connect to Redshift
- execute SQL
- validate SQL against a database
- inspect schemas
- provide autocomplete
- guarantee full Redshift compatibility
- fully support f-strings
- fully support Jinja templates
- format every possible SQL string
