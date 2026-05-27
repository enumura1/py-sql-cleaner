# Changelog

## 0.1.1 - 2026-05-26

Patch release focused on release-readiness and safety hardening.

- Add `py-sql-cleaner --version`.
- Keep f-strings, Jinja-like templates, and runtime placeholders skipped for both
  `format` and `extract`.
- Improve MySQL, Postgres, and Redshift smoke coverage and Redshift keyword
  detection.
- Align package layers with the documented CLI/application/domain/infrastructure
  architecture.
- Fix release packaging so build caches are not included in the source
  distribution.

## 0.1.0 - 2026-05-24

Initial MVP release.

- Detect SQL embedded in Python triple-quoted strings.
- Format safe embedded SQL with SQLGlot.
- Extract embedded SQL into `.sql` files and replace Python strings with file references.
- Skip f-strings and Jinja-like templates conservatively.
- Support explicit SQLGlot dialect selection with `--dialect` / `-d` for `generic`, `mysql`, `postgres`, and `redshift`.
- Preserve Redshift `COPY` and `UNLOAD` command-style statements instead of rewriting load/export options.
- Provide `list`, `format`, `check`, `extract`, and `dialects` CLI commands.
- Add documentation, CI checks, package build validation, and GitHub Pages docs.
