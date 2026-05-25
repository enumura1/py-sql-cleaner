from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from py_sql_cleaner.application.inspect_sql import SqlBlockReport, sql_block_report
from py_sql_cleaner.application.ports import SqlFormatter
from py_sql_cleaner.domain.detector import detect_sql_blocks
from py_sql_cleaner.domain.errors import FormatterError
from py_sql_cleaner.domain.models import SqlBlock
from py_sql_cleaner.domain.rewriter import replace_sql_content
from py_sql_cleaner.domain.safety import ALWAYS_SKIP_UNSAFE_REASONS, unsafe_reason


@dataclass(frozen=True)
class FormatSourceResult:
    source: str
    blocks: list[SqlBlockReport]
    warnings: list[str]
    errors: list[str]


def format_source(
    source_file: Path,
    source: str,
    *,
    dialect: str,
    backend: str,
    include_unsafe: bool,
    formatter: SqlFormatter,
) -> FormatSourceResult:
    blocks = detect_sql_blocks(source_file, source)
    result = _format_blocks(
        source,
        blocks,
        dialect=dialect,
        backend=backend,
        include_unsafe=include_unsafe,
        formatter=formatter,
    )
    return FormatSourceResult(
        source=result.source,
        blocks=[sql_block_report(block) for block in blocks],
        warnings=result.warnings,
        errors=result.errors,
    )


@dataclass(frozen=True)
class _FormatBlocksResult:
    source: str
    warnings: list[str]
    errors: list[str]


def _format_blocks(
    source: str,
    blocks: list[SqlBlock],
    *,
    dialect: str,
    backend: str,
    include_unsafe: bool,
    formatter: SqlFormatter,
) -> _FormatBlocksResult:
    warnings: list[str] = []
    errors: list[str] = []
    new_source = source
    for block in reversed(blocks):
        reason = unsafe_reason(block)
        if reason and (not include_unsafe or reason in ALWAYS_SKIP_UNSAFE_REASONS):
            warnings.append(
                f"Skipped unsafe SQL block {block.file_path}:{block.start_line}-"
                f"{block.end_line} reason={reason}"
            )
            continue
        try:
            formatted = formatter(block.raw_sql, dialect, backend)
        except FormatterError as exc:
            errors.append(
                f"failed to format SQL block {block.file_path}:{block.start_line}-"
                f"{block.end_line} with {backend}: {exc}. Skipping."
            )
            continue
        new_source = replace_sql_content(new_source, block, formatted)
    return _FormatBlocksResult(source=new_source, warnings=warnings, errors=errors)
