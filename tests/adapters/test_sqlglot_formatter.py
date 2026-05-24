import pytest

from py_sql_cleaner.adapters.sqlglot_formatter import format_sql
from py_sql_cleaner.domain.errors import FormatterError


def test_formats_with_clause() -> None:
    sql = """
with base as (
  select user_id, updated_at
  from users
)
select *
from base;
"""

    formatted = format_sql(sql)

    assert "WITH" in formatted
    assert "SELECT" in formatted
    assert formatted.endswith(";")


def test_defaults_to_generic_sqlglot_dialect() -> None:
    sql = """
select * from users;
"""

    formatted = format_sql(sql)

    assert "SELECT" in formatted
    assert "FROM users" in formatted


def test_formats_with_postgres_dialect() -> None:
    sql = """
select payload->>'name' as name
from events;
"""

    formatted = format_sql(sql, dialect="postgres")

    assert "payload ->> 'name'" in formatted
    assert "FROM events" in formatted


def test_formats_with_mysql_dialect() -> None:
    sql = """
select `user_id`
from `users`;
"""

    formatted = format_sql(sql, dialect="mysql")

    assert "`user_id`" in formatted
    assert "FROM `users`" in formatted


def test_formats_with_sqlglot_dialect_settings() -> None:
    sql = """
select * from users;
"""

    formatted = format_sql(sql, dialect="postgres, normalization_strategy=case_sensitive")

    assert "SELECT" in formatted
    assert "FROM users" in formatted


def test_formats_qualify_without_removing_window_clause() -> None:
    sql = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1;
"""

    formatted = format_sql(sql)

    assert "QUALIFY" in formatted
    assert "ROW_NUMBER" in formatted
    assert "PARTITION BY" in formatted


def test_formats_with_qualify() -> None:
    sql = """
with base as (
  select user_id, updated_at
  from users
)
select *
from base
qualify row_number() over(partition by user_id order by updated_at desc)=1;
"""

    formatted = format_sql(sql)

    assert "WITH" in formatted
    assert "QUALIFY" in formatted
    assert "ROW_NUMBER" in formatted


def test_formats_copy_without_dropping_redshift_clauses() -> None:
    sql = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
IGNOREHEADER 1;
"""

    formatted = format_sql(sql, dialect="redshift")

    assert "COPY users" in formatted
    assert "IAM_ROLE" in formatted
    assert "IGNOREHEADER 1" in formatted


def test_redshift_copy_command_is_preserved_without_rewriting_options() -> None:
    sql = """COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
TIMEFORMAT 'auto'
IGNOREHEADER 1;"""

    formatted = format_sql(sql, dialect="redshift")

    assert formatted == sql


def test_redshift_specific_command_requires_explicit_redshift_dialect() -> None:
    sql = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV;
"""

    with pytest.raises(FormatterError, match="requires --dialect redshift"):
        format_sql(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "select copy_count from users;",
        "select encoded_payload from events;",
        "select 'COPY' as word from events;",
        "select * from users where note = 'unload complete';",
        'select "COPY" from events;',
    ],
)
def test_redshift_keyword_detection_ignores_identifiers_and_literals(sql: str) -> None:
    formatted = format_sql(sql)

    assert "SELECT" in formatted


def test_unload_is_preserved_even_when_sqlglot_uses_command_fallback() -> None:
    sql = """
UNLOAD ('SELECT * FROM users')
TO '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS PARQUET;
"""

    formatted = format_sql(sql, dialect="redshift")

    assert "UNLOAD" in formatted
    assert "TO '<s3-path>'" in formatted
    assert "FORMAT AS PARQUET" in formatted


def test_unsupported_backend_raises_formatter_error() -> None:
    with pytest.raises(FormatterError):
        format_sql("select * from users", backend="unknown")


def test_unsupported_dialect_raises_formatter_error() -> None:
    with pytest.raises(FormatterError, match="unsupported SQL dialect"):
        format_sql("select * from users", dialect="unknown")


def test_unreviewed_sqlglot_dialect_raises_formatter_error() -> None:
    with pytest.raises(FormatterError, match="generic, mysql, postgres, redshift"):
        format_sql("select * from users", dialect="snowflake")
