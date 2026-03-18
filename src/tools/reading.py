"""Reading tools for MCP server"""

import json

from models import CoreProperties, DocumentInfo, ParagraphInfo, TableInfo
from utils import cell_text, load, paragraph_to_dict


def read_docx(path: str) -> str:
    """
    Extract the full text content of a .docx file.

    Args:
        path: Absolute path to the .docx file.

    Returns:
        Plain text of the document, paragraphs separated by newlines.
    """
    doc = load(path)
    return "\n".join(para.text for para in doc.paragraphs)


def get_document_info(path: str) -> str:
    """
    Return structural metadata about a .docx file: paragraph count, table
    count, section count, styles used, per-table info (index, rows, columns),
    and core properties (author, title, subject, created, modified, etc.).

    Args:
        path: Absolute path to the .docx file.

    Returns:
        JSON string with document metadata.
    """
    doc = load(path)
    cp = doc.core_properties
    info = DocumentInfo(
        paragraph_count=len(doc.paragraphs),
        table_count=len(doc.tables),
        section_count=len(doc.sections),
        styles_used=sorted({p.style.name for p in doc.paragraphs}),
        tables=[
            TableInfo(table_index=i, rows=len(t.rows), columns=len(t.columns))
            for i, t in enumerate(doc.tables)
        ],
        core_properties=CoreProperties(
            title=cp.title,
            author=cp.author,
            subject=cp.subject,
            keywords=cp.keywords,
            comments=cp.comments,
            created=str(cp.created) if cp.created else None,
            modified=str(cp.modified) if cp.modified else None,
            last_modified_by=cp.last_modified_by,
        ),
    )
    return info.model_dump_json(indent=2)


def list_paragraphs(path: str, start: int = 0, end: int | None = None) -> str:
    """
    List paragraphs with their index, style, and text.
    Useful before editing to identify the target paragraph index.

    Args:
        path: Absolute path to the .docx file.
        start: First paragraph index to include (0-based, default 0).
        end: Last paragraph index (exclusive). Omit to list all.

    Returns:
        JSON array of paragraph objects.
    """
    doc = load(path)
    paras = doc.paragraphs[start:end]
    result: list[ParagraphInfo] = [
        paragraph_to_dict(p, start + i) for i, p in enumerate(paras)
    ]
    return json.dumps([p.model_dump_json() for p in result], indent=2)


def read_table(path: str, table_index: int = 0) -> str:
    """
    Extract the contents of a specific table as a 2-D array.

    Args:
        path: Absolute path to the .docx file.
        table_index: Zero-based index of the table (default 0).

    Returns:
        JSON array of rows; each row is an array of cell text strings.
    """
    doc = load(path)
    if table_index >= len(doc.tables):
        raise IndexError(
            f"Table index {table_index} out of range "
            f"(document has {len(doc.tables)} table(s))."
        )
    tbl = doc.tables[table_index]
    rows: list[list[str]] = [
        [cell_text(cell) for cell in row.cells] for row in tbl.rows
    ]
    return json.dumps(rows, indent=2)


def list_styles(path: str) -> str:
    """
    List all styles defined in a .docx file, grouped by type.

    Args:
        path: Path to the .docx file.

    Returns:
        JSON object mapping style-type name to a sorted list of style names.
    """
    doc = load(path)
    groups: dict[str, list[str]] = {}
    for style in doc.styles:
        type_name = style.type.name if style.type else "UNKNOWN"
        groups.setdefault(type_name, []).append(style.name)
    for k in groups:
        groups[k].sort()
    return json.dumps(groups, indent=2)
