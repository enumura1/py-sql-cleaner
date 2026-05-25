from __future__ import annotations

from py_sql_cleaner.domain.models import SqlBlock

ALWAYS_SKIP_UNSAFE_REASONS = {"f-string", "jinja", "placeholder"}


def unsafe_reason(block: SqlBlock) -> str | None:
    if block.is_f_string:
        return "f-string"
    if block.has_jinja:
        return "jinja"
    if block.has_placeholder:
        return "placeholder"
    return None


def is_unsafe(block: SqlBlock) -> bool:
    return unsafe_reason(block) is not None
