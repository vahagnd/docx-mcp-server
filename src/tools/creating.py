"""Creating tools for MCP server"""

from pathlib import Path
from typing import Optional

from docx import Document

from utils import save


def create_docx(
    path: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    overwrite: bool = False,
) -> str:
    """
    Create a new, empty .docx file.

    Args:
        path:      Destination path (must end with .docx).
        title:     Optional document title stored in core properties.
        author:    Optional author name stored in core properties.
        overwrite: If False (default), raise an error if the file already exists.

    Returns:
        Confirmation message with the file path.
    """
    p = Path(path)
    if p.exists() and not overwrite:
        raise FileExistsError(
            f"{path} already exists. Pass overwrite=True to replace it."
        )
    doc = Document()
    if title:
        doc.core_properties.title = title
    if author:
        doc.core_properties.author = author
    save(doc, path)
    return f"Created: {path}"
