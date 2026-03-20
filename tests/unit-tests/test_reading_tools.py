import json

import pytest

from src.tools.reading import (
    get_document_info,
    list_paragraphs,
    list_styles,
    read_docx,
    read_table,
)


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


# =============================================================================


@pytest.mark.parametrize(
    "docx_path, expected_exception, flag",
    [
        ("rich_docx_path", None, "rich"),
        ("empty_docx_path", None, "empty"),
        ("nonexistent_docx_path", FileNotFoundError, None),
        ("not_docx_path", ValueError, None),
    ],
    ids=["rich", "empty", "nonexistent", "not_a_docx"],
)
def test_get_document(docx_path, expected_exception, flag, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            get_document_info(docx_path)
        return

    result = json.loads(get_document_info(docx_path))
    if flag == "rich":
        assert result["paragraph_count"] == 2
        assert result["table_count"] == 1
        assert result["section_count"] == 1
        assert "Heading 1" in result["styles_used"]
        assert "Normal" in result["styles_used"]
        table = result["tables"][0]
        assert table["table_index"] == 0
        assert table["rows"] == 2
        assert table["columns"] == 3
    elif flag == "empty":
        assert result["paragraph_count"] == 0
        assert result["table_count"] == 0
        assert result["section_count"] == 1
        assert result["styles_used"] == []
        assert result["tables"] == []
    assert "title" in result["core_properties"]
    assert "author" in result["core_properties"]


# =============================================================================


@pytest.mark.parametrize(
    "docx_path, expected_exception, start, end, flag",
    [
        ("rich_docx_path", None, 0, None, "all"),
        ("rich_docx_path", None, 1, None, "slice"),
        ("rich_docx_path", None, 0, 1, "start_end"),
        ("empty_docx_path", None, 0, None, "empty"),
        ("nonexistent_docx_path", FileNotFoundError, 0, None, None),
        ("not_docx_path", ValueError, 0, None, None),
    ],
    ids=["all", "slice", "start_end", "empty", "nonexistent", "not_a_docx"],
)
def test_list_paragraphs(docx_path, expected_exception, start, end, flag, request):
    docx_path = request.getfixturevalue(docx_path)
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            list_paragraphs(docx_path, start=start, end=end)
        return

    result = json.loads(list_paragraphs(docx_path, start=start, end=end))
    print(f"{result=}\n")
    if flag == "all":
        assert len(result) == 2
        assert result[0]["index"] == 0
        assert result[0]["text"] == "Hello"
        assert result[1]["index"] == 1
        assert result[1]["text"] == "World"
    elif flag == "slice":
        assert len(result) == 1
        assert result[0]["index"] == 1
        assert result[0]["text"] == "World"
    elif flag == "start_end":
        assert len(result) == 1
        assert result[0]["text"] == "Hello"
    elif flag == "empty":
        assert result == []


# =============================================================================


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


# =============================================================================


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
