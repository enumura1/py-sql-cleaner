from pathlib import Path

from py_sql_cleaner.domain.detector import detect_sql_blocks, has_runtime_placeholder


def test_detects_triple_quoted_query_assignment() -> None:
    source = '''query = """
select * from users
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].variable_name == "query"
    assert blocks[0].confidence == 0.95
    assert blocks[0].raw_sql.strip() == "select * from users"


def test_detects_sql_suffix_variable() -> None:
    source = '''load_users_sql = """
select * from users
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].variable_name == "load_users_sql"


def test_detects_single_quote_triple_string() -> None:
    source = """sql = '''
select * from users
'''
"""

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].quote == "'''"


def test_marks_f_string_as_unsafe() -> None:
    source = '''query = f"""
select * from users where id = {user_id}
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].is_f_string is True


def test_marks_jinja_like_sql() -> None:
    source = '''query = """
select * from users where ds = '{{ ds }}'
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].has_jinja is True


def test_marks_runtime_placeholders() -> None:
    source = '''query = """
select * from users where id = :user_id and status = %s
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].has_placeholder is True


def test_marks_pyformat_runtime_placeholder() -> None:
    source = '''query = """
select * from users where id = %(user_id)s
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].has_placeholder is True


def test_marks_python_format_fields_as_runtime_placeholders() -> None:
    source = '''query = """
select * from users where id = {user_id}
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].has_placeholder is True


def test_placeholder_detection_ignores_escaped_python_format_braces() -> None:
    sql = """
select '{{ literal }}' as value
from events
"""

    assert has_runtime_placeholder(sql) is False


def test_placeholder_detection_ignores_literals_comments_and_postgres_casts() -> None:
    sql = """
select created_at::date as day, ':literal' as value
from events
where note = '100%s'
-- where id = :commented
/* where id = %(commented)s */
"""

    assert has_runtime_placeholder(sql) is False


def test_detects_redshift_copy_statement() -> None:
    source = '''query = """
COPY users
FROM '<s3-path>'
IAM_ROLE '<iam-role-arn>'
FORMAT AS CSV
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
    assert blocks[0].confidence == 0.95


def test_detects_postgres_operator_statement() -> None:
    source = '''query = """
select payload->>'name' as name
from events
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1


def test_detects_mysql_backtick_statement() -> None:
    source = '''query = """
select `user_id`
from `users`
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1


def test_detects_command_style_sql_from_query_variable() -> None:
    source = '''query = """
truncate table staging_users
"""
'''

    blocks = detect_sql_blocks(Path("foo.py"), source)

    assert len(blocks) == 1
