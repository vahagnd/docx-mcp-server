"""Reading tools core functions"""

from src.models import (
    CoreProperties,
    DocumentInfo,
    ListReturn,
    ParagraphInfo,
    StyleGroups,
    TableInfo,
)
from src.utils import cell_text, load, paragraph_to_dict


def read_docx(path: str) -> ListReturn:
    doc = load(path)
    return ListReturn([para.text for para in doc.paragraphs])


def get_document_info(path: str) -> DocumentInfo:
    doc = load(path)
    cp = doc.core_properties
    return DocumentInfo(
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


def list_paragraphs(
    path: str, start: int = 0, end: int | None = None
) -> ListReturn[ParagraphInfo]:
    doc = load(path)
    paras = doc.paragraphs[start:end]
    return ListReturn([paragraph_to_dict(p, start + i) for i, p in enumerate(paras)])


def read_table(path: str, table_index: int = 0) -> ListReturn[list[str]]:
    doc = load(path)
    if table_index >= len(doc.tables):
        raise IndexError(
            f"Table index {table_index} out of range "
            f"(document has {len(doc.tables)} table(s))."
        )
    tbl = doc.tables[table_index]
    rows = ListReturn([cell_text(cell) for cell in row.cells] for row in tbl.rows)
    return rows


def list_styles(path: str) -> StyleGroups:
    doc = load(path)
    groups: dict[str, list[str]] = {}
    for style in doc.styles:
        type_name = style.type.name if style.type else "UNKNOWN"
        groups.setdefault(type_name, []).append(style.name)
    for k in groups:
        groups[k].sort()
    return StyleGroups(groups)
