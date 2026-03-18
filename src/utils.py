from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import _Cell
from docx.text.paragraph import Paragraph

from models import ParagraphInfo

ALIGN_MAP = {
    "left": WD_ALIGN_PARAGRAPH.LEFT,
    "center": WD_ALIGN_PARAGRAPH.CENTER,
    "right": WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}


def load(path: str) -> DocumentObject:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if p.suffix.lower() != ".docx":
        raise ValueError(f"Not a .docx file: {path}")
    return Document(str(p))


def save(doc: DocumentObject, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def paragraph_to_dict(para: Paragraph, index: int) -> ParagraphInfo:
    return ParagraphInfo(
        index=index,
        style=para.style.name,
        text=para.text,
        alignment=str(para.alignment) if para.alignment else None,
    )


def cell_text(cell: _Cell) -> str:
    return "\n".join(p.text for p in cell.paragraphs)


def resolve_align(alignment: str) -> WD_ALIGN_PARAGRAPH:
    align = ALIGN_MAP.get(alignment.lower())
    if align is None:
        raise ValueError(f"Unknown alignment '{alignment}'. Use: {list(ALIGN_MAP)}")
    return align
