from __future__ import annotations

from dataclasses import dataclass

from py_sql_cleaner.application.ports import SqlFormatter
from py_sql_cleaner.core.rewriter import replace_sql_content
from py_sql_cleaner.domain.errors import FormatterError
from py_sql_cleaner.domain.models import SqlBlock

ALWAYS_SKIP_UNSAFE_REASONS = {"f-string", "jinja"}


@dataclass(frozen=True)
class FormatSourceResult:
    source: str
    warnings: list[str]
    errors: list[str]


def format_source(
    source: str,
    blocks: list[SqlBlock],
    *,
    dialect: str,
    backend: str,
    include_unsafe: bool,
    formatter: SqlFormatter,
) -> FormatSourceResult:
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
    return FormatSourceResult(source=new_source, warnings=warnings, errors=errors)


def unsafe_reason(block: SqlBlock) -> str | None:
    if block.is_f_string:
        return "f-string"
    if block.has_jinja:
        return "jinja"
    return None


def is_unsafe(block: SqlBlock) -> bool:
    return unsafe_reason(block) is not None
