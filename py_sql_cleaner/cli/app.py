from __future__ import annotations

import difflib
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from py_sql_cleaner.adapters.sqlglot_formatter import (
    SUPPORTED_DIALECTS,
    format_sql,
    get_formatter_backend,
    normalize_dialect,
)
from py_sql_cleaner.application.extract_sql import plan_extract
from py_sql_cleaner.application.format_source import format_source, is_unsafe
from py_sql_cleaner.core.detector import detect_sql_blocks
from py_sql_cleaner.domain.config import DEFAULT_BACKEND, DEFAULT_DIALECT
from py_sql_cleaner.domain.errors import FormatterError

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("list")
def list_blocks(file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]) -> None:
    source = file.read_text(encoding="utf-8")
    blocks = detect_sql_blocks(file, source)
    if not blocks:
        console.print("No embedded SQL blocks found.")
        return

    console.print(f"Found {len(blocks)} SQL blocks")
    for number, block in enumerate(blocks, start=1):
        console.print()
        console.print(f"{number}. {block.file_path}:{block.start_line}-{block.end_line}")
        console.print(f"   variable: {block.variable_name or '-'}")
        console.print(f"   confidence: {block.confidence:.2f}")
        console.print(f"   unsafe: {str(is_unsafe(block)).lower()}")


@app.command("format")
def format_command(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    dialect: Annotated[
        str,
        typer.Option("--dialect", help="SQLGlot dialect to use for parsing and formatting."),
    ] = DEFAULT_DIALECT,
    backend: Annotated[str, typer.Option()] = DEFAULT_BACKEND,
    write: Annotated[bool, typer.Option("--write/--check")] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    include_unsafe: Annotated[bool, typer.Option("--include-unsafe")] = False,
) -> None:
    _validate_formatter_options(dialect, backend)
    source = file.read_text(encoding="utf-8")
    blocks = detect_sql_blocks(file, source)
    if not blocks:
        console.print("No embedded SQL blocks found.")
        raise typer.Exit(0)

    try:
        result = format_source(
            source,
            blocks,
            dialect=dialect,
            backend=backend,
            include_unsafe=include_unsafe,
            formatter=format_sql,
        )
    except FormatterError as exc:
        console.print(f"Error: {exc}")
        raise typer.Exit(1) from exc
    for warning in result.warnings:
        console.print(f"Warning: {warning}")

    changed = result.source != source
    if dry_run:
        _print_diff(file, source, result.source)
        raise typer.Exit(1 if not write and changed else 0)
    if not write:
        if changed:
            console.print("Found unformatted embedded SQL:")
            for block in blocks:
                console.print(
                    f"- {block.file_path}:{block.start_line}-{block.end_line} "
                    f"variable={block.variable_name or '-'}"
                )
            raise typer.Exit(1)
        raise typer.Exit(0)

    if changed:
        file.write_text(result.source, encoding="utf-8")
        console.print(f"Formatted {file}")


@app.command("check")
def check_command(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    dialect: Annotated[
        str,
        typer.Option("--dialect", help="SQLGlot dialect to use for parsing and formatting."),
    ] = DEFAULT_DIALECT,
    backend: Annotated[str, typer.Option()] = DEFAULT_BACKEND,
) -> None:
    format_command(file, dialect=dialect, backend=backend, write=False, dry_run=False)


@app.command("extract")
def extract_command(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    out_dir: Annotated[Path, typer.Option("--out-dir")] = Path("sql"),
    dialect: Annotated[
        str,
        typer.Option("--dialect", help="SQLGlot dialect to use for extracted SQL."),
    ] = DEFAULT_DIALECT,
    backend: Annotated[str, typer.Option()] = DEFAULT_BACKEND,
    replace_mode: Annotated[str, typer.Option("--replace-mode")] = "path",
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    name: Annotated[str | None, typer.Option("--name")] = None,
) -> None:
    _validate_formatter_options(dialect, backend)
    source = file.read_text(encoding="utf-8")
    blocks = detect_sql_blocks(file, source)
    if not blocks:
        console.print("No embedded SQL blocks found.")
        raise typer.Exit(0)
    if name and len(blocks) > 1:
        console.print("Error: --name can only be used when exactly one SQL block is detected.")
        raise typer.Exit(1)

    try:
        result = plan_extract(
            file,
            source,
            blocks,
            out_dir=out_dir,
            dialect=dialect,
            backend=backend,
            replace_mode=replace_mode,
            name=name,
            formatter=format_sql,
        )
    except FormatterError as exc:
        console.print(f"Error: {exc}")
        raise typer.Exit(1) from exc
    for warning in result.warnings:
        console.print(f"Warning: {warning}")

    if not result.replacements:
        raise typer.Exit(0)

    if dry_run:
        for replacement in result.replacements:
            console.print(f"Would write {replacement.output_path}")
        _print_diff(file, source, result.source)
        raise typer.Exit(0)

    for replacement in result.replacements:
        _write_sql_file_at_path(replacement.output_path, replacement.sql)
        console.print(f"Wrote {replacement.output_path}")

    file.write_text(result.source, encoding="utf-8")
    if replace_mode == "read-text":
        console.print("Warning: replace-mode=read-text requires `from pathlib import Path`.")


@app.command("dialects")
def dialects_command() -> None:
    """List SQL dialect values accepted by --dialect."""
    for dialect in SUPPORTED_DIALECTS:
        console.print(dialect)


def _print_diff(file: Path, old: str, new: str) -> None:
    if old == new:
        console.print("No changes.")
        return
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=str(file),
        tofile=str(file),
        lineterm="",
    )
    console.print("\n".join(diff))


def _validate_formatter_options(dialect: str, backend: str) -> None:
    try:
        normalize_dialect(dialect)
        get_formatter_backend(backend)
    except FormatterError as exc:
        console.print(f"Error: {exc}")
        raise typer.Exit(1) from exc


def _write_sql_file_at_path(path: Path, sql: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_ensure_trailing_newline(sql), encoding="utf-8")


def _ensure_trailing_newline(sql: str) -> str:
    return sql if sql.endswith("\n") else f"{sql}\n"
