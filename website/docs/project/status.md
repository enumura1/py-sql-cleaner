---
sidebar_position: 2
---

# Project Status

`py-sql-cleaner` is currently an early MVP. The `0.1.x` release line is intended
for early use and feedback, not long-term compatibility guarantees.

The current focus is:

- Python files
- triple-quoted SQL strings
- SQLGlot-backed SQL formatting, defaulting to generic SQL with `--dialect`
  support for explicitly enabled database-specific formatting
- formatting
- extracting SQL into `.sql` files

Future versions may add:

- additional SQL dialects based on user demand
- database-specific validation beyond SQLGlot formatting
- better template handling
- safer f-string handling
- pre-commit integration
- more configurable formatting backends
- editor integrations

## Video

A walkthrough video will be added here later.
