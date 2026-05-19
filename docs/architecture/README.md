# Architecture

`py-sql-cleaner` is intentionally small, but the package still has explicit
boundaries. The goal is to keep the CLI easy to change while making the SQL
detection, rewriting, and formatting behavior testable without Rich, Typer, or
filesystem concerns leaking everywhere.

## Layers

Dependency direction is top to bottom:

```text
py_sql_cleaner.cli
py_sql_cleaner.application
py_sql_cleaner.adapters
py_sql_cleaner.core
py_sql_cleaner.domain
```

The layers are enforced by `import-linter`.

### `domain`

Owns stable concepts shared by the rest of the package:

- `SqlBlock`
- package errors
- default configuration values

This layer must stay independent of Typer, Rich, SQLGlot, and other package
layers. It should be boring and easy to import from tests.

### `core`

Owns deterministic source-level logic:

- token-based embedded SQL detection
- SQL file naming helpers
- Python source rewriting

Core code may depend on `domain`, but it must not depend on CLI libraries,
terminal rendering, or command behavior.

### `adapters`

Owns external tool integrations. SQLGlot is currently isolated in
`adapters/sqlglot_formatter.py` so a future formatter backend or dialect policy
does not force the application flow or CLI to change.

### `application`

Owns use cases:

- format these detected blocks
- plan extraction of these blocks into SQL files
- decide what is skipped and which warnings should be returned

Application functions receive dependencies, such as the SQL formatter, through
plain function arguments typed in `application/ports.py`. This is dependency
injection without adding a DI container. It is enough for this package because
the dependency graph is small and mostly functional.

### `cli`

Owns human-facing input and output:

- Typer command definitions
- file reads and writes
- Rich console messages
- unified diff printing

CLI code can call lower layers, but lower layers must not know that Typer or
Rich exists.

## Why This Shape

This is a small layered architecture, not enterprise scaffolding. The tradeoff
is deliberate:

- We keep only five directories because the package has three workflows: list,
  format, and extract.
- We avoid repository classes and DI containers because there is no database,
  long-lived service, or runtime object graph.
- We isolate SQLGlot because formatter behavior is the most likely extension
  point.
- We forbid `application` from importing `adapters` so use cases stay testable
  with a fake formatter.
- We keep file writes at the CLI boundary so the core logic can be tested as
  string and path transformations.
- We enforce imports in CI and pre-push so coding agents cannot silently turn
  the package back into one large script directory.

## Harness

Run the full local harness before pushing:

```bash
scripts/check
```

The harness runs:

- `ruff format --check .`
- `ruff check .`
- `lint-imports`
- `pytest`
- website build, when `website/package.json` exists
- package build
- `twine check dist/*`

The repository also provides `.githooks/pre-push`. Enable it once:

```bash
git config core.hooksPath .githooks
```
