"""Reading tools for MCP server"""

from src.core import reading


def read_docx(path: str) -> str:
    """
    Extract the full text content of a .docx file.

    Args:
        path: Absolute path to the .docx file.

    Returns:
        Plain text of the document, paragraphs separated by newlines.
    """
    return "\n".join(reading.read_docx(path).root)


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
    return reading.get_document_info(path).model_dump_json(indent=2)


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
    return reading.list_paragraphs(path, start, end).model_dump_json()


def read_table(path: str, table_index: int = 0) -> str:
    """
    Extract the contents of a specific table as a 2-D array.

    Args:
        path: Absolute path to the .docx file.
        table_index: Zero-based index of the table (default 0).

    Returns:
        JSON array of rows; each row is an array of cell text strings.
    """
    return reading.read_table(path, table_index).model_dump_json()


def list_styles(path: str) -> str:
    """
    List all styles defined in a .docx file, grouped by type.

    Args:
        path: Path to the .docx file.

    Returns:
        JSON object mapping style-type name to a sorted list of style names.
    """
    return reading.list_styles(path).model_dump_json()
