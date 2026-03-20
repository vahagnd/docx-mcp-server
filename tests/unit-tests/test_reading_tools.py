import json

import pytest

from src.tools.reading import (
    get_document_info,
    list_paragraphs,
    list_styles,
    read_docx,
    read_table,
)


# ----- read_docx -----
@pytest.mark.parametrize(
    "docx_path, expected_result, expected_exception",
    [
        ("simple_docx_path", "Hello\nWorld", None),
        ("empty_docx_path", "", None),
        ("nonexistent_docx_path", None, FileNotFoundError),
        ("not_docx_path", None, ValueError),
    ],
    ids=["simple", "empty", "nonexistent", "not_a_docx"],
)
def test_read_docx(docx_path, expected_result, expected_exception, request):
    docx_path = request.getfixturevalue(docx_path)

    if expected_exception is not None:
        with pytest.raises(expected_exception):
            read_docx(docx_path)
        return

    result = read_docx(docx_path)
    assert result == expected_result


# ----- get_document -----
@pytest.mark.parametrize(
    "docx_path, expected_exception",
    [
        ("simple_docx_path", None),
        ("nonexistent_docx_path", FileNotFoundError),
        ("not_docx_path", ValueError),
    ],
    ids=["simple", "nonexistent", "not_docx"],
)
def test_get_document(docx_path, expected_exception, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            get_document_info(docx_path)
        return

    result = json.loads(get_document_info(docx_path))
    assert "title" in result["core_properties"]
    assert "author" in result["core_properties"]


def test_get_document_rich(rich_docx_path):
    result = json.loads(get_document_info(rich_docx_path))
    assert result["paragraph_count"] == 2
    assert result["table_count"] == 1
    assert result["section_count"] == 1
    assert "Heading 1" in result["styles_used"]
    assert "Normal" in result["styles_used"]
    table = result["tables"][0]
    assert table["table_index"] == 0
    assert table["rows"] == 2
    assert table["columns"] == 3


def test_get_document_empty(empty_docx_path):
    result = json.loads(get_document_info(empty_docx_path))
    assert result["paragraph_count"] == 0
    assert result["table_count"] == 0
    assert result["section_count"] == 1
    assert result["styles_used"] == []
    assert result["tables"] == []


# ----- list_paragraphs -----
@pytest.mark.parametrize(
    "docx_path, expected_exception",
    [
        ("simple_docx_path", None),
        ("nonexistent_docx_path", FileNotFoundError),
        ("not_docx_path", ValueError),
    ],
    ids=["simple", "nonexistent", "not_docx"],
)
def test_list_paragraphs(docx_path, expected_exception, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            list_paragraphs(docx_path)
        return

    result = json.loads(list_paragraphs(docx_path))
    assert isinstance(result, list)


def test_list_paragraphs_all(rich_docx_path):
    result = json.loads(list_paragraphs(rich_docx_path))
    assert len(result) == 2
    assert result[0]["index"] == 0
    assert result[0]["text"] == "Hello"
    assert result[1]["index"] == 1
    assert result[1]["text"] == "World"


def test_list_paragraphs_slice(rich_docx_path):
    result = json.loads(list_paragraphs(rich_docx_path, start=1))
    assert len(result) == 1
    assert result[0]["index"] == 1
    assert result[0]["text"] == "World"


def test_list_paragraphs_start_end(rich_docx_path):
    result = json.loads(list_paragraphs(rich_docx_path, start=0, end=1))
    assert len(result) == 1
    assert result[0]["text"] == "Hello"


def test_list_paragraphs_empty(empty_docx_path):
    result = json.loads(list_paragraphs(empty_docx_path))
    assert result == []


# ----- read_table -----
@pytest.mark.parametrize(
    "docx_path, expected_exception, table_index",
    [
        ("table_docx_path", None, 0),
        ("table_docx_path", IndexError, 5),
        ("empty_docx_path", IndexError, 0),
        ("nonexistent_docx_path", FileNotFoundError, 0),
        ("not_docx_path", ValueError, 0),
    ],
    ids=["table", "table_index_out_of_range", "empty", "nonexistent", "not_a_docx"],
)
def test_read_table(docx_path, expected_exception, table_index, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            read_table(docx_path, table_index=table_index)
        return

    result = json.loads(read_table(docx_path, table_index=table_index))
    assert result == [["A", "B", "C"], ["D", "E", "F"]]


# ----- list_styles -----
@pytest.mark.parametrize(
    "docx_path, expected_exception",
    [
        ("simple_docx_path", None),
        ("nonexistent_docx_path", FileNotFoundError),
        ("not_docx_path", ValueError),
    ],
    ids=["simple", "nonexistent", "not_a_docx"],
)
def test_list_styles(docx_path, expected_exception, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            list_styles(docx_path)
        return

    result = json.loads(list_styles(docx_path))
    assert "PARAGRAPH" in result
    assert "CHARACTER" in result
    assert "Normal" in result["PARAGRAPH"]

    for styles in result.values():
        assert styles == sorted(styles)
