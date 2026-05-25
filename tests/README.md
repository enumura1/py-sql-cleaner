# Test Organization

Tests are grouped by the package boundary or user-facing surface they exercise:

- `cli/` tests Typer command behavior and filesystem effects owned by commands.
- `application/` tests use-case flow when behavior is not already covered by CLI tests.
- `domain/` tests py-sql-cleaner rules such as SQL detection and source rewriting.
- `infrastructure/` tests external integrations such as SQLGlot formatting.
- `fixtures/` contains input files shared by tests.

When adding tests, place them next to the responsibility being verified instead
of adding more files directly under `tests/`.
