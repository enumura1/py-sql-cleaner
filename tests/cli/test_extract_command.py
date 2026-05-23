from typer.testing import CliRunner

from py_sql_cleaner.cli import app

runner = CliRunner()


def test_extract_writes_sql_file_and_replaces_python_string(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select * from users
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["extract", str(file), "--out-dir", "sql"])

    assert result.exit_code == 0, result.output
    sql_file = tmp_path / "sql" / "query.sql"
    assert sql_file.exists()
    assert "SELECT" in sql_file.read_text(encoding="utf-8")
    assert file.read_text(encoding="utf-8") == 'query = "sql/query.sql"\n'


def test_extract_accepts_explicit_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select payload->>'name' as name
from events
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["extract", str(file), "--out-dir", "sql", "--dialect", "postgres"],
    )

    assert result.exit_code == 0, result.output
    sql_file = tmp_path / "sql" / "query.sql"
    assert "payload ->> 'name'" in sql_file.read_text(encoding="utf-8")


def test_extract_accepts_mysql_dialect(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select `user_id`
from `users`
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["extract", str(file), "--out-dir", "sql", "-d", "mysql"],
    )

    assert result.exit_code == 0, result.output
    sql_file = tmp_path / "sql" / "query.sql"
    assert "`user_id`" in sql_file.read_text(encoding="utf-8")
    assert "FROM `users`" in sql_file.read_text(encoding="utf-8")


def test_extract_accepts_redshift_dialect(tmp_path) -> None:
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

    result = runner.invoke(
        app,
        ["extract", str(file), "--out-dir", "sql", "-d", "redshift"],
    )

    assert result.exit_code == 0, result.output
    sql_file = tmp_path / "sql" / "query.sql"
    sql = sql_file.read_text(encoding="utf-8")
    assert "COPY users" in sql
    assert "IAM_ROLE" in sql
    assert "IGNOREHEADER 1" in sql


def test_extract_dry_run_does_not_modify_files(tmp_path) -> None:
    file = tmp_path / "foo.py"
    original = '''query = """
select * from users
"""
'''
    file.write_text(original, encoding="utf-8")

    result = runner.invoke(app, ["extract", str(file), "--out-dir", "sql", "--dry-run"])

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == original
    assert not (tmp_path / "sql").exists()
    assert "Would write" in result.output


def test_extract_read_text_mode(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select * from users
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["extract", str(file), "--out-dir", "sql", "--replace-mode", "read-text"],
    )

    assert result.exit_code == 0, result.output
    assert file.read_text(encoding="utf-8") == 'query = Path("sql/query.sql").read_text()\n'
    assert "requires `from pathlib import Path`" in result.output


def test_extract_avoids_name_collisions_within_same_run(tmp_path) -> None:
    file = tmp_path / "foo.py"
    file.write_text(
        '''query = """
select * from users
"""

query = """
select * from events
"""
''',
        encoding="utf-8",
    )

    result = runner.invoke(app, ["extract", str(file), "--out-dir", "sql"])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "sql" / "query.sql").exists()
    assert (tmp_path / "sql" / "query_2.sql").exists()
    assert file.read_text(encoding="utf-8") == (
        'query = "sql/query.sql"\n\nquery = "sql/query_2.sql"\n'
    )
