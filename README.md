# py-sql-cleaner

`py-sql-cleaner` is a CLI tool for finding, formatting, and extracting SQL
embedded in Python files.

It is built for Python codebases where long SQL queries are written directly
inside triple-quoted Python strings. The current MVP uses SQLGlot for formatting,
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

`py-sql-cleaner` is an early MVP. It uses SQLGlot internally for best-effort SQL
formatting. It does not connect to databases and does not execute SQL.
Dialect support means SQLGlot parser/formatter mode selection, not exhaustive
database validation. Redshift command-style statements such as `COPY` and
`UNLOAD` are preserved rather than reformatted to avoid changing load/export
options.

> [!NOTE]
> `py-sql-cleaner` is conservative by default: f-strings and Jinja-like templates are
> detected but skipped instead of being rewritten.

## Features

- Format SQL embedded in Python triple-quoted strings
- Extract embedded SQL into external `.sql` files
- Replace embedded SQL strings with file references
- Detect common SQL variable names such as `sql`, `query`, `*_sql`, and
  `*_query`
- Skip unsafe blocks, including f-strings and Jinja-like templates, by default
- Support explicit dialect selection with `--dialect` / `-d`
- Support `check` mode for CI
- Support `dry-run` mode before rewriting files

## Installation

Install `py-sql-cleaner` from
[PyPI](https://pypi.org/project/py-sql-cleaner/):

```bash
pip install py-sql-cleaner
```

Or install it as an isolated CLI tool with `pipx`:

```bash
pipx install py-sql-cleaner
```

Release archives and wheels are also attached to
[GitHub Releases](https://github.com/enumura1/py-sql-cleaner/releases).

You can also run it without installing:

```bash
uvx py-sql-cleaner --help
```

## Quick Start

1. List embedded SQL blocks:

   ```bash
   py-sql-cleaner list jobs/load_users.py
   ```

2. Preview formatting changes:

   ```bash
   py-sql-cleaner format jobs/load_users.py --dry-run
   ```

3. Format embedded SQL in place:

   ```bash
   py-sql-cleaner format jobs/load_users.py
   ```

4. Format with a database-specific dialect:

   ```bash
   py-sql-cleaner format jobs/load_users.py -d redshift
   ```

   Currently enabled dialects are `generic`, `mysql`, `postgres`, and
   `redshift`.

5. Extract embedded SQL into `.sql` files:

   ```bash
   py-sql-cleaner extract jobs/load_users.py --out-dir sql
   ```

6. Check formatting for CI:

   ```bash
   py-sql-cleaner check jobs/load_users.py
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

After `py-sql-cleaner format jobs/load_users.py`:

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

After `py-sql-cleaner extract jobs/load_users.py --out-dir sql`:

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

`py-sql-cleaner` is conservative by default. It skips unsafe blocks instead of
rewriting them.

> [!NOTE]
> Skipped blocks are left unchanged. This is intentional: preserving runtime
> behavior is more important than formatting every SQL-looking string.

Always skipped by `format` and `extract`:

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

f-strings and Jinja-like templates are not complete SQL at rest. Python or a
template engine fills those values at runtime, so rewriting or extracting the
file contents directly could change runtime behavior.

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

## Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `list` | List embedded SQL blocks | `py-sql-cleaner list jobs/load_users.py` |
| `format` | Format embedded SQL in place | `py-sql-cleaner format jobs/load_users.py` |
| `check` | Check whether embedded SQL is formatted | `py-sql-cleaner check jobs/load_users.py` |
| `extract` | Extract embedded SQL into `.sql` files | `py-sql-cleaner extract jobs/load_users.py --out-dir sql` |
| `dialects` | List accepted dialect values | `py-sql-cleaner dialects` |

Use `py-sql-cleaner --version` to print the installed CLI version.

## Documentation

- [Documentation site source](website/docs/intro.md)
- [Usage Guide](website/docs/getting-started/quick-start.md)
- [Safety and Limitations](website/docs/project/safety.md)
- [Contributing](CONTRIBUTING.md)

## Status

`py-sql-cleaner` is currently an early MVP.

The current focus is:

- Python files
- triple-quoted SQL strings
- SQLGlot-backed SQL formatting, defaulting to generic SQL with `--dialect`
  support for explicitly enabled database-specific formatting
- formatting
- extracting SQL into `.sql` files

## License

MIT
