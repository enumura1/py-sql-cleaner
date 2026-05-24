# Test Organization

Tests are grouped by the package boundary or user-facing surface they exercise:

- `adapters/` tests external integrations such as SQLGlot formatting.
- `cli/` tests Typer command behavior and filesystem effects owned by commands.
- `core/` tests deterministic detection, extraction, and rewriting logic.
- `fixtures/` contains input files shared by tests.

When adding tests, place them next to the responsibility being verified instead
of adding more files directly under `tests/`.
