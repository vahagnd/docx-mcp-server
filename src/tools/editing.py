"""Editing tools for MCP server"""

import copy
import json
import re
from typing import Optional

from utils import load, resolve_align, save


def find_replace(
    path: str,
    find: str,
    replace: str,
    case_sensitive: bool = True,
) -> str:
    """
    Find and replace all occurrences of a string across paragraphs and tables.
    Operates run-by-run to preserve existing formatting.

    Args:
        path:           Path to the .docx file.
        find:           Text to search for.
        replace:        Replacement text.
        case_sensitive: Whether the search is case-sensitive (default True).

    Returns:
        JSON with 'replacements' count.
    """
    doc = load(path)
    count = 0

    def _replace_in_para(para):
        nonlocal count
        for run in para.runs:
            if case_sensitive:
                occurrences = run.text.count(find)
                if occurrences:
                    run.text = run.text.replace(find, replace)
                    count += occurrences
            else:
                occurrences = run.text.lower().count(find.lower())
                if occurrences:
                    run.text = re.sub(
                        re.escape(find), replace, run.text, flags=re.IGNORECASE
                    )
                    count += occurrences

    for para in doc.paragraphs:
        _replace_in_para(para)
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    _replace_in_para(para)

    save(doc, path)
    return json.dumps({"replacements": count})


def update_paragraph(
    path: str,
    index: int,
    text: Optional[str] = None,
    style: Optional[str] = None,
    bold: Optional[bool] = None,
    italic: Optional[bool] = None,
    alignment: Optional[str] = None,
) -> str:
    """
    Update the text and/or formatting of an existing paragraph by index.

    Args:
        path:      Path to the .docx file.
        index:     Zero-based index of the paragraph to update.
        text:      New text (replaces all existing runs if provided).
        style:     New paragraph style name.
        bold:      Set bold on all runs.
        italic:    Set italic on all runs.
        alignment: "left" | "center" | "right" | "justify".

    Returns:
        Confirmation message.
    """
    doc = load(path)
    if not 0 <= index < len(doc.paragraphs):
        raise IndexError(f"Index {index} out of range (0–{len(doc.paragraphs) - 1}).")
    para = doc.paragraphs[index]

    if text is not None:
        for run in para.runs:
            run.text = ""
        if para.runs:
            para.runs[0].text = text
        else:
            para.add_run(text)

    if style:
        para.style = style

    if bold is not None or italic is not None:
        for run in para.runs:
            if bold is not None:
                run.bold = bold
            if italic is not None:
                run.italic = italic

    if alignment:
        para.alignment = resolve_align(alignment)

    save(doc, path)
    return f"Paragraph {index} updated."


def delete_paragraph(path: str, index: int) -> str:
    """
    Delete a paragraph by index.

    Args:
        path:  Path to the .docx file.
        index: Zero-based index of the paragraph to remove.

    Returns:
        Confirmation message.
    """
    doc = load(path)
    if not 0 <= index < len(doc.paragraphs):
        raise IndexError(f"Index {index} out of range (0–{len(doc.paragraphs) - 1}).")
    elem = doc.paragraphs[index]._element
    elem.getparent().remove(elem)
    save(doc, path)
    return f"Paragraph {index} deleted."


def set_core_properties(
    path: str,
    title: Optional[str] = None,
    author: Optional[str] = None,
    subject: Optional[str] = None,
    keywords: Optional[str] = None,
    comments: Optional[str] = None,
) -> str:
    """
    Set core document properties (metadata) on an existing .docx file.

    Args:
        path:     Path to the .docx file.
        title:    Document title.
        author:   Author name.
        subject:  Document subject.
        keywords: Comma-separated keywords.
        comments: Document comments / description.

    Returns:
        JSON with the updated properties.
    """
    doc = load(path)
    cp = doc.core_properties
    if title is not None:
        cp.title = title
    if author is not None:
        cp.author = author
    if subject is not None:
        cp.subject = subject
    if keywords is not None:
        cp.keywords = keywords
    if comments is not None:
        cp.comments = comments
    save(doc, path)
    return json.dumps(
        {
            "title": cp.title,
            "author": cp.author,
            "subject": cp.subject,
            "keywords": cp.keywords,
            "comments": cp.comments,
        },
        indent=2,
    )


def merge_documents(
    base_path: str,
    other_path: str,
    output_path: str,
    add_page_break_between: bool = True,
) -> str:
    """
    Append the contents of a second .docx file to a first one and save
    the result to a new file.

    Args:
        base_path:              Path to the base document.
        other_path:             Path to the document to append.
        output_path:            Where to save the merged document.
        add_page_break_between: Insert a page break between documents (default True).

    Returns:
        Confirmation message with the output path.
    """
    base = load(base_path)
    other = load(other_path)
    if add_page_break_between:
        base.add_page_break()
    for element in other.element.body:
        if element.tag.endswith(
            "}sectPr"
        ):  # skip section properties to avoid layout conflicts
            continue
        base.element.body.append(copy.deepcopy(element))
    save(base, output_path)
    return f"Merged '{base_path}' + '{other_path}' → '{output_path}'."
