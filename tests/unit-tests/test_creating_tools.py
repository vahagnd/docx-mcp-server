import json
from pathlib import Path

import pytest
from docx import Document

from src.tools.creating import create_docx


@pytest.mark.parametrize(
    "docx_path, expected_exception",
    [
        ("new_docx_path", None),
        ("simple_docx_path", FileExistsError),
        ("new_not_docx_path", ValueError),
    ],
    ids=["new_docx", "existing_docx", "new_not_docx"],
)
def test_create_docx(docx_path, expected_exception, request):
    docx_path = request.getfixturevalue(docx_path)

    if expected_exception:
        with pytest.raises(expected_exception):
            create_docx(docx_path)
        return

    result = json.loads(create_docx(docx_path, title="My Title", author="John"))
    assert result["path"] == docx_path
    assert result["title"] == "My Title"
    assert result["author"] == "John"
    assert Path(docx_path).exists()

    doc = Document(docx_path)
    assert doc.core_properties.title == "My Title"
    assert doc.core_properties.author == "John"


def test_create_docx_overwrite(simple_docx_path):
    result = json.loads(create_docx(simple_docx_path, overwrite=True))
    assert result["path"] == simple_docx_path
