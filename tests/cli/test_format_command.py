from typer.testing import CliRunner

from py_sql_cleaner.cli import app

runner = CliRunner()


def test_version_option_prints_package_version() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0, result.output
    assert "py-sql-cleaner 0.1.0" in result.output


def test_format_command_rewrites_embedded_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file)])

    assert result.exit_code == 0, result.output
    source = file.read_text(encoding="utf-8")
    assert "SELECT" in source
    assert "QUALIFY" in source
    assert "ROW_NUMBER" in source
    assert "PARTITION BY" in source


def test_format_command_accepts_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select payload->>'name' as name
from events
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file), "--dialect", "postgres"])

    assert result.exit_code == 0, result.output
    source = file.read_text(encoding="utf-8")
    assert "payload ->> 'name'" in source
    assert "FROM events" in source


def test_format_command_preserves_redshift_copy_with_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
IGNOREHEADER 1
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file), "-d", "redshift"])

    assert result.exit_code == 0, result.output
    source = file.read_text(encoding="utf-8")
    assert "COPY users" in source
    assert "IAM_ROLE" in source
    assert "IGNOREHEADER 1" in source


def test_format_command_rejects_redshift_copy_without_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
IGNOREHEADER 1
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file)])

    assert result.exit_code == 1
    assert "requires --dialect redshift" in result.output
    assert file.read_text(encoding="utf-8") == original


def test_check_returns_one_for_redshift_copy_without_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
IGNOREHEADER 1
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["check", str(file)])

    assert result.exit_code == 1
    assert "requires --dialect redshift" in result.output


def test_format_command_preserves_mysql_backticks_with_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select `user_id`
from `users`
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file), "-d", "mysql"])

    assert result.exit_code == 0, result.output
    source = file.read_text(encoding="utf-8")
    assert "`user_id`" in source
    assert "FROM `users`" in source


def test_format_command_accepts_short_dialect_option(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select payload->>'name' as name
from events
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file), "-d", "postgres"])

    assert result.exit_code == 0, result.output
    assert "payload ->> 'name'" in file.read_text(encoding="utf-8")


def test_format_command_rejects_unknown_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select * from users
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["format", str(file), "--dialect", "unknown"])

    assert result.exit_code == 1
    assert "unsupported SQL dialect" in result.output
    assert "generic" in result.output
    assert "mysql" in result.output
    assert "postgres" in result.output
    assert "redshift" in result.output


def test_dialects_command_lists_supported_dialects() -> None:
    result = runner.invoke(app, ["dialects"])

    assert result.exit_code == 0, result.output
    assert "generic" in result.output
    assert "mysql" in result.output
    assert "postgres" in result.output
    assert "redshift" in result.output
    assert "snowflake" not in result.output


def test_format_dry_run_does_not_modify_file(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file), "--dry-run"])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "SELECT" in result.output


def test_check_returns_one_for_unformatted_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select * from users
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["check", str(file)])

    assert result.exit_code == 1
    assert "Found unformatted embedded SQL" in result.output


def test_format_skips_jinja_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users where ds = '{{ ds }}'
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file)])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "reason=jinja" in result.output


def test_format_include_unsafe_still_skips_f_string_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = f"""
select * from users where id = {user_id}
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file), "--include-unsafe"])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "reason=f-string" in result.output


def test_format_include_unsafe_still_skips_jinja_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users where ds = '{{ ds }}'
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file), "--include-unsafe"])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "reason=jinja" in result.output


def test_format_skips_named_runtime_placeholder_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users where id = :user_id
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file)])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "reason=placeholder" in result.output


def test_format_include_unsafe_still_skips_placeholder_sql(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users where id = %s and email = %(email)s
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["format", str(file), "--include-unsafe"])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert "reason=placeholder" in result.output
