from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

import sqlglot
from sqlglot.dialects import Dialect
from sqlglot.tokens import Tokenizer, TokenType

from py_sql_cleaner.domain.config import DEFAULT_BACKEND, DEFAULT_DIALECT
from py_sql_cleaner.domain.errors import FormatterError

SUPPORTED_DIALECTS = ("generic", "mysql", "postgres", "redshift")
REDSHIFT_EXPLICIT_DIALECT_KEYWORDS = (
    "COPY",
    "UNLOAD",
    "IAM_ROLE",
    "DISTKEY",
    "SORTKEY",
    "DISTSTYLE",
    "ENCODE",
)
REDSHIFT_PRESERVE_COMMANDS = ("COPY", "UNLOAD")


class FormatterBackend(ABC):
    @abstractmethod
    def format(self, sql: str, dialect: str) -> str:
        raise NotImplementedError


class SqlglotFormatter(FormatterBackend):
    def format(self, sql: str, dialect: str) -> str:
        dialect = normalize_dialect(dialect)
        if not dialect and _has_redshift_explicit_dialect_keyword(sql):
            raise FormatterError("redshift-specific SQL requires --dialect redshift")
        if _dialect_name(dialect) == "redshift" and _starts_with_command(
            sql, REDSHIFT_PRESERVE_COMMANDS
        ):
            return sql.strip()
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
    if normalized == "generic":
        return ""
    dialect_name = normalized.split(",", maxsplit=1)[0].strip()
    if dialect_name not in SUPPORTED_DIALECTS:
        supported = ", ".join(SUPPORTED_DIALECTS)
        raise FormatterError(f"unsupported SQL dialect: {dialect}. Supported dialects: {supported}")
    try:
        Dialect.get_or_raise(normalized)
    except Exception as exc:
        raise FormatterError(f"unsupported SQL dialect: {dialect}. {exc}") from exc
    return normalized


def _dialect_name(dialect: str) -> str:
    return dialect.split(",", maxsplit=1)[0].strip().lower()


def _has_redshift_explicit_dialect_keyword(sql: str) -> bool:
    return any(token.text.upper() in REDSHIFT_EXPLICIT_DIALECT_KEYWORDS for token in _word_tokens(sql))


def _starts_with_command(sql: str, commands: tuple[str, ...]) -> bool:
    first_token = next(iter(_word_tokens(sql)), None)
    return bool(first_token and first_token.text.upper() in commands)


def _word_tokens(sql: str) -> Iterator:
    return (
        token
        for token in Tokenizer().tokenize(sql)
        if token.token_type not in {TokenType.IDENTIFIER, TokenType.STRING, TokenType.UNKNOWN}
        and not _is_backtick_quoted_token(sql, token)
    )


def _is_backtick_quoted_token(sql: str, token) -> bool:
    return token.start > 0 and token.end + 1 < len(sql) and sql[token.start - 1] == "`" and sql[
        token.end + 1
    ] == "`"


def get_formatter_backend(backend: str) -> FormatterBackend:
    if backend != DEFAULT_BACKEND:
        raise FormatterError(f"unsupported formatter backend: {backend}")
    return SqlglotFormatter()


def format_sql(sql: str, dialect: str = DEFAULT_DIALECT, backend: str = DEFAULT_BACKEND) -> str:
    return get_formatter_backend(backend).format(sql.strip(), dialect=dialect)
