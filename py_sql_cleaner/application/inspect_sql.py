from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from py_sql_cleaner.domain.detector import detect_sql_blocks
from py_sql_cleaner.domain.models import SqlBlock
from py_sql_cleaner.domain.safety import is_unsafe


@dataclass(frozen=True)
class SqlBlockReport:
    file_path: Path
    start_line: int
    end_line: int
    variable_name: str | None
    confidence: float
    unsafe: bool


def inspect_sql_blocks(source_file: Path, source: str) -> list[SqlBlockReport]:
    return [sql_block_report(block) for block in detect_sql_blocks(source_file, source)]


def sql_block_report(block: SqlBlock) -> SqlBlockReport:
    return SqlBlockReport(
        file_path=block.file_path,
        start_line=block.start_line,
        end_line=block.end_line,
        variable_name=block.variable_name,
        confidence=block.confidence,
        unsafe=is_unsafe(block),
    )
