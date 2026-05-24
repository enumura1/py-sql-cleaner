from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

import sqlglot
from sqlglot.dialects import Dialect
from sqlglot.tokens import Tokenizer, TokenType

from py_sql_cleaner.domain.config import DEFAULT_BACKEND, DEFAULT_DIALECT
from py_sql_cleaner.domain.errors import FormatterError

SUPPORTED_DIALECTS = ("generic", "mysql", "postgres", "redshift")
REDSHIFT_TABLE_OPTION_KEYWORDS = (
    "DISTKEY",
    "SORTKEY",
    "DISTSTYLE",
)
REDSHIFT_PRESERVE_COMMANDS = ("COPY", "UNLOAD")
REDSHIFT_COLUMN_OPTION_KEYWORDS = ("ENCODE",)


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
    tokens = list(_word_tokens(sql))
    if _starts_with_command_tokens(tokens, REDSHIFT_PRESERVE_COMMANDS):
        return True
    return any(
        _is_redshift_explicit_dialect_token(tokens, index)
        for index, token in enumerate(tokens)
        if token.text.upper() in REDSHIFT_TABLE_OPTION_KEYWORDS + REDSHIFT_COLUMN_OPTION_KEYWORDS
    )


def _starts_with_command(sql: str, commands: tuple[str, ...]) -> bool:
    return _starts_with_command_tokens(list(_word_tokens(sql)), commands)


def _starts_with_command_tokens(tokens: list, commands: tuple[str, ...]) -> bool:
    first_token = next(iter(tokens), None)
    return bool(first_token and first_token.text.upper() in commands)


def _is_redshift_explicit_dialect_token(tokens: list, index: int) -> bool:
    token_text = tokens[index].text.upper()
    if token_text in REDSHIFT_TABLE_OPTION_KEYWORDS:
        return _looks_like_table_option(tokens, index)
    if token_text in REDSHIFT_COLUMN_OPTION_KEYWORDS:
        return _looks_like_table_option(tokens, index)
    return False


def _looks_like_table_option(tokens: list, index: int) -> bool:
    previous_token = tokens[index - 1].text.upper() if index > 0 else ""
    next_token = tokens[index + 1].text.upper() if index + 1 < len(tokens) else ""
    return previous_token not in {"", ",", "SELECT", "AS"} and next_token not in {
        "",
        ",",
        "FROM",
    }


def _word_tokens(sql: str) -> Iterator:
    return (
        token
        for token in Tokenizer().tokenize(sql)
        if token.token_type not in {TokenType.IDENTIFIER, TokenType.STRING, TokenType.UNKNOWN}
        and not _is_backtick_quoted_token(sql, token)
    )


def _is_backtick_quoted_token(sql: str, token) -> bool:
    return (
        token.start > 0
        and token.end + 1 < len(sql)
        and sql[token.start - 1] == "`"
        and sql[token.end + 1] == "`"
    )


def get_formatter_backend(backend: str) -> FormatterBackend:
    if backend != DEFAULT_BACKEND:
        raise FormatterError(f"unsupported formatter backend: {backend}")
    return SqlglotFormatter()


def format_sql(sql: str, dialect: str = DEFAULT_DIALECT, backend: str = DEFAULT_BACKEND) -> str:
    return get_formatter_backend(backend).format(sql.strip(), dialect=dialect)
