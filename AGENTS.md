# Coding Agent Instructions

Start here, then open the referenced docs only when they are relevant to the
change.

## Project Map

- Architecture: `docs/architecture/README.md`
- Branch workflow: `docs/development/branching.md`
- Test layout: `tests/README.md`
- Contributor workflow: `CONTRIBUTING.md`

## Dependency Rules

The only allowed inward dependency direction is:

```text
cli -> application -> adapters -> core -> domain
```

Upper layers may skip downward when it keeps the code simple, but lower layers
must never import upward.

- `domain` must not import package layers, Typer, Rich, or SQLGlot.
- `core` must not import CLI code, Typer, or Rich.
- `application` should receive formatter behavior through
  `application/ports.py` and function arguments.
- `application` must not import `adapters`, Typer, Rich, or SQLGlot directly.
- `adapters` is where external formatter implementations live.
- `cli` is the only layer that should own Typer commands, Rich output, and file
  writes caused by commands.

Use `import-linter` to enforce these rules. Do not bypass it with local import
hacks.

## Change Discipline

- Keep changes small and behavior-focused.
- Add or update tests for behavior changes.
- Do not add a DI container. Pass dependencies as function arguments unless the
  object graph becomes meaningfully more complex.
- Keep SQLGlot usage isolated behind `py_sql_cleaner.adapters`.
- Run `scripts/check` before pushing.
