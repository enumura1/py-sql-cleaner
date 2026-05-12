---
sidebar_position: 1
---

# Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `list` | List embedded SQL blocks | `pyredsql list jobs/load_users.py` |
| `format` | Format embedded SQL in place | `pyredsql format jobs/load_users.py` |
| `check` | Check whether embedded SQL is formatted | `pyredsql check jobs/load_users.py` |
| `extract` | Extract embedded SQL into `.sql` files | `pyredsql extract jobs/load_users.py --out-dir sql` |

## `list`

```bash
pyredsql list path/to/file.py
```

## `format`

```bash
pyredsql format path/to/file.py
```

Preview changes:

```bash
pyredsql format path/to/file.py --dry-run
```

## `check`

```bash
pyredsql check path/to/file.py
```

## `extract`

```bash
pyredsql extract path/to/file.py --out-dir sql
```

Use `read-text` replacement mode:

```bash
pyredsql extract path/to/file.py --out-dir sql --replace-mode read-text
```

Result:

```python
query = Path("sql/query.sql").read_text()
```

:::note
`pyredsql` does not automatically insert `from pathlib import Path` in the
current MVP.
:::

Specify an output name:

```bash
pyredsql extract path/to/file.py --out-dir sql --name load_users
```
