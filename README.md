# pyredsql

`pyredsql` is a Redshift-first CLI tool for formatting and extracting SQL
embedded in Python files.

It is built for Python codebases where long Redshift SQL queries are written
directly inside triple-quoted Python strings.

```python
query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
```

`pyredsql` can format that SQL in place, or extract it into an external `.sql`
file.

`pyredsql` is an early MVP. It uses SQLGlot internally for best-effort SQL
formatting. It does not connect to databases and does not execute SQL.

## Features

- Format Redshift SQL embedded in Python triple-quoted strings
- Extract embedded SQL into external `.sql` files
- Replace embedded SQL strings with file references
- Detect common SQL variable names such as `sql`, `query`, `*_sql`, and
  `*_query`
- Skip unsafe blocks, including f-strings and Jinja-like templates, by default
- Support `check` mode for CI
- Support `dry-run` mode before rewriting files

## Installation

```bash
pip install pyredsql
```

Or install it as an isolated CLI tool:

```bash
pipx install pyredsql
```

You can also run it without installing:

```bash
uvx pyredsql --help
```

## Quick Start

List embedded SQL blocks:

```bash
pyredsql list jobs/load_users.py
```

Preview formatting changes:

```bash
pyredsql format jobs/load_users.py --dry-run
```

Format embedded SQL in place:

```bash
pyredsql format jobs/load_users.py
```

Extract embedded SQL into `.sql` files:

```bash
pyredsql extract jobs/load_users.py --out-dir sql
```

Check formatting for CI:

```bash
pyredsql check jobs/load_users.py
```

## Example

Before:

```python
query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
```

After `pyredsql format jobs/load_users.py`:

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

After `pyredsql extract jobs/load_users.py --out-dir sql`:

```python
query = "sql/query.sql"
```

## Supported Input

The current MVP targets Python triple-quoted strings.

Supported:

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

Not targeted in the MVP:

```python
query = "SELECT * FROM users"
```

## Safety

`pyredsql` is conservative by default. It skips unsafe blocks instead of
rewriting them.

Skipped by default:

```python
query = f"""
SELECT *
FROM users
WHERE user_id = {user_id}
"""
```

```python
query = """
SELECT *
FROM users
WHERE ds = '{{ ds }}'
"""
```

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

## Commands

| Command | Purpose |
| --- | --- |
| `pyredsql list FILE` | List embedded SQL blocks |
| `pyredsql format FILE` | Format embedded SQL in place |
| `pyredsql check FILE` | Check whether embedded SQL is formatted |
| `pyredsql extract FILE --out-dir sql` | Extract embedded SQL into `.sql` files |

## Documentation

- [Usage Guide](docs/usage.md)
- [Safety and Limitations](docs/safety.md)
- [Contributing](CONTRIBUTING.md)

## Status

`pyredsql` is currently an early MVP.

The current focus is:

- Python files
- triple-quoted SQL strings
- Redshift SQL
- formatting
- extracting SQL into `.sql` files

## License

MIT
