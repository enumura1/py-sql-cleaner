from __future__ import annotations

from pathlib import Path

from py_sql_cleaner.domain.models import SqlBlock


def build_sql_file_name(block: SqlBlock, source_file: Path) -> str:
    if block.variable_name:
        stem = block.variable_name
        for suffix in ("_sql", "_query"):
            if stem.endswith(suffix):
                stem = stem[: -len(suffix)]
                break
        return f"{stem}.sql"
    return f"{source_file.stem}_l{block.start_line}.sql"


def unique_sql_path(out_dir: Path, file_name: str) -> Path:
    candidate = out_dir / _ensure_sql_suffix(file_name)
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        numbered = out_dir / f"{stem}_{counter}{suffix}"
        if not numbered.exists():
            return numbered
        counter += 1


def _ensure_sql_suffix(file_name: str) -> str:
    return file_name if file_name.endswith(".sql") else f"{file_name}.sql"
