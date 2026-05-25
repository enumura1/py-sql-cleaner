# Coding Agent Instructions

Start here, then open the referenced docs only when they are relevant to the
change.

## Project Map

- Architecture: `docs/architecture/README.md`
- Branch workflow: `docs/development/branching.md`
- Test layout: `tests/README.md`
- Contributor workflow: `CONTRIBUTING.md`

## Dependency Rules

The package uses a small layered architecture with a formatter port:

```text
                 cli / interface
          ┌──────────┴──────────┐
          v                     v
    application          infrastructure
          |                ┌────┴────┐
          v                v         v
        domain           domain    SQLGlot
```

`cli` wires the application use cases to the concrete infrastructure formatter.
It should not call domain logic directly.

- `domain` must not import package layers, Typer, Rich, or SQLGlot.
- `application` should receive formatter behavior through
  `application/ports.py` and function arguments.
- `application` must not import `infrastructure`, Typer, Rich, or SQLGlot directly.
- `infrastructure` is where external formatter implementations live.
- `cli` is the only layer that should own Typer commands, Rich output, and file
  writes caused by commands.
- `cli` may import `application` and `infrastructure`, but not `domain`.

Use `import-linter` to enforce these rules. Do not bypass it with local import
hacks.

## Change Discipline

- Keep changes small and behavior-focused.
- Add or update tests for behavior changes.
- Do not add a DI container. Pass dependencies as function arguments unless the
  object graph becomes meaningfully more complex.
- Keep SQLGlot usage isolated behind `py_sql_cleaner.infrastructure`.
- Run `scripts/check` before pushing.
