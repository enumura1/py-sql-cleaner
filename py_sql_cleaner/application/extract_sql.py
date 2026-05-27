from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from py_sql_cleaner.application.inspect_sql import SqlBlockReport, sql_block_report
from py_sql_cleaner.application.ports import SqlFormatter
from py_sql_cleaner.domain.detector import detect_sql_blocks
from py_sql_cleaner.domain.errors import FormatterError
from py_sql_cleaner.domain.extractor import build_sql_file_name
from py_sql_cleaner.domain.models import SqlBlock
from py_sql_cleaner.domain.rewriter import replace_sql_block_with_reference
from py_sql_cleaner.domain.safety import unsafe_reason as unsafe_block_reason


@dataclass(frozen=True)
class ExtractedSql:
    block: SqlBlock
    output_path: Path
    sql: str


@dataclass(frozen=True)
class ExtractPlan:
    source: str
    blocks: list[SqlBlockReport]
    replacements: list[ExtractedSql]
    warnings: list[str]


def plan_extract(
    source_file: Path,
    source: str,
    *,
    out_dir: Path,
    dialect: str,
    backend: str,
    replace_mode: str,
    name: str | None,
    formatter: SqlFormatter,
) -> ExtractPlan:
    blocks = detect_sql_blocks(source_file, source)
    if name and len(blocks) > 1:
        raise ValueError("--name can only be used when exactly one SQL block is detected.")

    output_dir = out_dir if out_dir.is_absolute() else source_file.parent / out_dir
    warnings: list[str] = []
    replacements: list[ExtractedSql] = []
    planned_paths: set[Path] = set()

    for block in blocks:
        unsafe_reason = unsafe_block_reason(block)
        if unsafe_reason:
            warnings.append(
                f"Skipped unsafe SQL block {source_file}:{block.start_line}-{block.end_line} "
                f"reason={unsafe_reason}"
            )
            continue

        file_name = _validated_name(name) if name else build_sql_file_name(block, source_file)
        output_path = unique_planned_sql_path(output_dir, file_name, planned_paths)
        planned_paths.add(output_path)

        sql = block.raw_sql.strip()
        try:
            sql = formatter(sql, dialect, backend)
        except FormatterError:
            warnings.append(
                "failed to format SQL block "
                f"{source_file}:{block.start_line}-{block.end_line} with {backend}. "
                "Writing original SQL."
            )
        replacements.append(ExtractedSql(block=block, output_path=output_path, sql=sql))

    new_source = source
    for replacement in reversed(replacements):
        reference = _reference_path(replacement.output_path, source_file.parent)
        new_source = replace_sql_block_with_reference(
            new_source,
            replacement.block,
            reference,
            replace_mode=replace_mode,
        )

    return ExtractPlan(
        source=new_source,
        blocks=[sql_block_report(block) for block in blocks],
        replacements=replacements,
        warnings=warnings,
    )


def _reference_path(output_path: Path, source_dir: Path) -> str:
    try:
        return output_path.relative_to(source_dir).as_posix()
    except ValueError:
        return output_path.as_posix()


def _validated_name(name: str) -> str:
    if not name or name in {".", ".."} or "\\" in name or Path(name).name != name:
        raise ValueError("--name must be a file name, not a path.")
    return name


def unique_planned_sql_path(out_dir: Path, file_name: str, planned_paths: set[Path]) -> Path:
    normalized_name = file_name if file_name.endswith(".sql") else f"{file_name}.sql"
    candidate = out_dir / normalized_name
    if not candidate.exists() and candidate not in planned_paths:
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 2
    while True:
        numbered = out_dir / f"{stem}_{counter}{suffix}"
        if not numbered.exists() and numbered not in planned_paths:
            return numbered
        counter += 1
