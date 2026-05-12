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

> [!NOTE]
> `pyredsql` is conservative by default: f-strings and Jinja-like templates are
> detected but skipped instead of being rewritten.

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

`pyredsql` is not published to PyPI yet. PyPI installation will be available
after the first package release.

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

1. List embedded SQL blocks:

   ```bash
   pyredsql list jobs/load_users.py
   ```

2. Preview formatting changes:

   ```bash
   pyredsql format jobs/load_users.py --dry-run
   ```

3. Format embedded SQL in place:

   ```bash
   pyredsql format jobs/load_users.py
   ```

4. Extract embedded SQL into `.sql` files:

   ```bash
   pyredsql extract jobs/load_users.py --out-dir sql
   ```

5. Check formatting for CI:

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

> [!NOTE]
> Skipped blocks are left unchanged. This is intentional: preserving runtime
> behavior is more important than formatting every SQL-looking string.

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

| Command | Purpose | Example |
| --- | --- | --- |
| `list` | List embedded SQL blocks | `pyredsql list jobs/load_users.py` |
| `format` | Format embedded SQL in place | `pyredsql format jobs/load_users.py` |
| `check` | Check whether embedded SQL is formatted | `pyredsql check jobs/load_users.py` |
| `extract` | Extract embedded SQL into `.sql` files | `pyredsql extract jobs/load_users.py --out-dir sql` |

## Documentation

- [Documentation site source](website/docs/intro.md)
- [Usage Guide](website/docs/getting-started/quick-start.md)
- [Safety and Limitations](website/docs/project/safety.md)
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
