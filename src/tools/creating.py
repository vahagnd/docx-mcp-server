"""Creating tools for MCP server"""

from typing import Optional

from src.core import creating


def create_docx(
    path: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    overwrite: bool = False,
) -> str:
    """
    Create a new, empty .docx file.

    Args:
        path: Full destination path (must end with .docx).
        title: Optional document title stored in core properties.
        author: Optional author name stored in core properties.
        overwrite: If False (default), raise an error if the file already exists.

    Returns:
        JSON confirmation object with path, title, and author of the created document.
    """
    return creating.create_docx(path, title, author, overwrite).model_dump_json()
