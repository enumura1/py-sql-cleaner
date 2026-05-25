# Architecture

`py-sql-cleaner` uses a small layered architecture for a CLI tool. The goal is
to keep command-line I/O, use-case flow, domain rules, and external library
integration separate enough to explain and test.

## Dependency Direction

```text
                 cli / interface
          ┌──────────┴──────────┐
          v                     v
    application          infrastructure
          |                ┌────┴────┐
          v                v         v
        domain           domain    SQLGlot
```

- `cli` is the interface layer and composition root.
- `application` implements use-case flow.
- `domain` owns py-sql-cleaner models and rules.
- `infrastructure` integrates with external libraries such as SQLGlot.
- `SQLGlot` is an external PyPI dependency, not a project layer.

`cli` may import `application` and `infrastructure`, but it should not call
`domain` directly. Domain logic is exercised through application use cases.

This is a normal layered shape for this CLI project:

```text
interface -> application -> domain
interface -> infrastructure -> external dependency
```

The project does not have a repository layer because it does not own a database,
ORM, queue, or external service client. File reads/writes are command-line I/O
and stay at the `cli` boundary.

## Layers

### `cli`

Owns user-facing input and output:

- Typer command definitions
- argument parsing
- file reads and writes
- Rich console messages
- unified diff printing
- wiring application use cases to the concrete infrastructure formatter

### `application`

Owns use cases:

- list SQL blocks
- format embedded SQL
- check formatting
- plan SQL extraction
- decide warnings and errors for command workflows

Application code uses domain rules and receives formatter behavior through
`application/ports.py`. It does not import SQLGlot or infrastructure directly.

### `domain`

Owns py-sql-cleaner-specific models and rules:

- `SqlBlock`
- SQL block detection in Python source
- unsafe block classification
- Python source rewriting
- SQL output file naming
- package errors and defaults

Domain code must not import CLI, application, infrastructure, Typer, Rich, or
SQLGlot.

Examples of domain decisions:

- f-strings, Jinja-like templates, and runtime placeholders are unsafe to
  rewrite.
- Python triple-quoted strings with enough SQL signal become `SqlBlock` values.
- Replacement ranges are calculated from Python source positions.

### `infrastructure`

Owns external technology integration:

- SQLGlot formatter implementation
- supported dialect normalization
- SQLGlot error translation
- Redshift command preservation around SQLGlot behavior

Infrastructure may import domain errors/config and SQLGlot. It must not import
CLI or application code.

SQLGlot is only used here. It is the external SQL parser/formatter engine that
turns SQL text into formatted SQL text. The infrastructure layer adapts SQLGlot's
API and quirks into the formatter callable that the application expects.

## Dependency Injection

Application use cases depend on a formatter callable:

```python
SqlFormatter = Callable[[str, str, str], str]
```

The CLI injects the concrete SQLGlot formatter from infrastructure when it calls
the use case. This keeps application logic independent from SQLGlot while
avoiding a DI container or stateful formatter object.

This is also the project's dependency-inversion point. Application code defines
the formatter shape it needs; infrastructure code adapts SQLGlot to that shape;
CLI wires the concrete function into the use case.

The formatter is injected as a function because it has no long-lived state:

- no database connection
- no credentials
- no transaction
- no cache
- no close/dispose lifecycle

If a future formatter needs state, it can be passed as an object that implements
the same callable shape.

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
