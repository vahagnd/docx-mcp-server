"""Creating tools core functions"""

from pathlib import Path

from docx import Document

from src.models import DocxCreated
from src.utils import save


def create_docx(
    path: str,
    title: str | None = None,
    author: str | None = None,
    overwrite: bool = False,
) -> DocxCreated:
    if Path(path).exists() and not overwrite:
        raise FileExistsError(
            f"{path} already exists. Pass overwrite=True to replace it."
        )
    doc = Document()
    if title:
        doc.core_properties.title = title
    if author:
        doc.core_properties.author = author
    save(doc, path)
    return DocxCreated(path=path, title=title, author=author)
