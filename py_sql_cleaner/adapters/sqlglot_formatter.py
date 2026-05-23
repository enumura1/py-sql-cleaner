from __future__ import annotations

from abc import ABC, abstractmethod

import sqlglot

from py_sql_cleaner.domain.config import DEFAULT_BACKEND, DEFAULT_DIALECT
from py_sql_cleaner.domain.errors import FormatterError

SUPPORTED_DIALECTS = tuple(sorted(dialect.value for dialect in sqlglot.Dialects if dialect.value))


class FormatterBackend(ABC):
    @abstractmethod
    def format(self, sql: str, dialect: str) -> str:
        raise NotImplementedError


class SqlglotFormatter(FormatterBackend):
    def format(self, sql: str, dialect: str) -> str:
        dialect = normalize_dialect(dialect)
        try:
            expressions = sqlglot.parse(sql, read=dialect)
            formatted = ";\n\n".join(expr.sql(dialect=dialect, pretty=True) for expr in expressions)
        except Exception as exc:
            raise FormatterError(str(exc)) from exc

        if sql.rstrip().endswith(";") and not formatted.rstrip().endswith(";"):
            formatted += ";"
        return formatted


def normalize_dialect(dialect: str) -> str:
    normalized = dialect.strip().lower()
    if normalized not in SUPPORTED_DIALECTS:
        supported = ", ".join(SUPPORTED_DIALECTS)
        raise FormatterError(f"unsupported SQL dialect: {dialect}. Supported dialects: {supported}")
    return normalized


def get_formatter_backend(backend: str) -> FormatterBackend:
    if backend != DEFAULT_BACKEND:
        raise FormatterError(f"unsupported formatter backend: {backend}")
    return SqlglotFormatter()


def format_sql(sql: str, dialect: str = DEFAULT_DIALECT, backend: str = DEFAULT_BACKEND) -> str:
    return get_formatter_backend(backend).format(sql.strip(), dialect=dialect)
