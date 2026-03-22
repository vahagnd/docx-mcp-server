from typing import Any

from pydantic import BaseModel, Field, RootModel


class ListReturn[T=Any](RootModel[list[T]]):
    root: list[T]


class ParagraphInfo(BaseModel):
    index: int = Field(
        description="Position of the paragraph in the document, starting from 0"
    )
    style: str = Field(
        description="Style name applied to the paragraph, e.g. 'Normal', 'Heading 1'"
    )
    text: str = Field(description="Full plain text content of the paragraph")
    alignment: str | None = Field(
        description="Horizontal text alignment, e.g. 'WD_ALIGN_PARAGRAPH.LEFT', or None if unset"
    )


class TableInfo(BaseModel):
    table_index: int = Field(
        description="Position of the table in the document, starting from 0"
    )
    rows: int = Field(description="Number of rows in the table")
    columns: int = Field(description="Number of columns in the table")


class CoreProperties(BaseModel):
    title: str | None = Field(description="Document title set in Word's properties")
    author: str | None = Field(description="Original author of the document")
    subject: str | None = Field(description="Subject field from document properties")
    keywords: str | None = Field(description="Keywords field from document properties")
    comments: str | None = Field(
        description="Description/comments field, not inline comments"
    )
    created: str | None = Field(
        description="Datetime when the document was first created"
    )
    modified: str | None = Field(description="Datetime of last modification")
    last_modified_by: str | None = Field(
        description="Username of whoever last saved the document"
    )


class DocumentInfo(BaseModel):
    paragraph_count: int = Field(
        description="Total number of paragraph blocks in the document body"
    )
    table_count: int = Field(description="Total number of tables")
    section_count: int = Field(
        description="Total number of sections; each can have its own page size, margins, orientation"
    )
    styles_used: list[str] = Field(
        description="Alphabetically sorted list of unique style names applied to paragraphs"
    )
    tables: list[TableInfo] = Field(description="Per-table structural info")
    core_properties: CoreProperties = Field(
        description="Word's built-in document metadata"
    )


class StyleGroups(RootModel):
    root: dict[str, list[str]]


class DocxCreated(BaseModel):
    path: str = Field(description="Absolute path to the created .docx file.")
    title: str | None = Field(default=None, description="Document title stored in core properties.")
    author: str | None = Field(default=None, description="Author name stored in core properties.")
