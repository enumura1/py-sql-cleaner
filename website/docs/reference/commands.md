---
sidebar_position: 1
---

# Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `list` | List embedded SQL blocks | `py-sql-cleaner list jobs/load_users.py` |
| `format` | Format embedded SQL in place | `py-sql-cleaner format jobs/load_users.py` |
| `check` | Check whether embedded SQL is formatted | `py-sql-cleaner check jobs/load_users.py` |
| `extract` | Extract embedded SQL into `.sql` files | `py-sql-cleaner extract jobs/load_users.py --out-dir sql` |
| `dialects` | List accepted SQLGlot dialect values | `py-sql-cleaner dialects` |

## `list`

```bash
py-sql-cleaner list path/to/file.py
```

## `format`

```bash
py-sql-cleaner format path/to/file.py
```

Use a database-specific SQLGlot dialect:

```bash
py-sql-cleaner format path/to/file.py -d redshift
```

Preview changes:

```bash
py-sql-cleaner format path/to/file.py --dry-run
```

## `check`

```bash
py-sql-cleaner check path/to/file.py
```

Use the same dialect option as `format`:

```bash
py-sql-cleaner check path/to/file.py -d snowflake
```

## `extract`

```bash
py-sql-cleaner extract path/to/file.py --out-dir sql
```

Format extracted SQL with a database-specific dialect:

```bash
py-sql-cleaner extract path/to/file.py --out-dir sql -d postgres
```

Use `read-text` replacement mode:

```bash
py-sql-cleaner extract path/to/file.py --out-dir sql --replace-mode read-text
```

Result:

```python
query = Path("sql/query.sql").read_text()
```

:::note
`py-sql-cleaner` does not automatically insert `from pathlib import Path` in the
current MVP.
:::

Specify an output name:

```bash
py-sql-cleaner extract path/to/file.py --out-dir sql --name load_users
```

## `dialects`

```bash
py-sql-cleaner dialects
```

The output lists the SQLGlot dialect values accepted by `--dialect`.
