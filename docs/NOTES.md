## What can be in .docx file

- Paragraphs
- Tables
- Images / shapes / drawings
- Text boxes
- Headers / footers
- Footnotes / endnotes
- Comments
- Embedded objects (Excel charts, etc.)
- Bookmarks / hyperlinks
- Form fields


## Tools

### `reading.get_document_info` returns

```json
{
  "paragraph_count": "total number of paragraph blocks in the document body",
  "table_count": "total number of tables",
  "section_count": "total number of sections; each section can have its own page size, margins, orientation",
  "styles_used": "alphabetically sorted list of unique style names applied to paragraphs e.g. ['Heading 1', 'Normal', 'Title']",
  "tables": [
    {
      "table_index": "position of the table in the document, starting from 0",
      "rows": "number of rows in that table",
      "columns": "number of columns in that table"
    }
  ],
  "core_properties": {
    "title": "document title set in Word's properties",
    "author": "original author",
    "subject": "subject field",
    "keywords": "keywords field",
    "comments": "description/comments field (not inline comments)",
    "created": "datetime when the document was first created",
    "modified": "datetime of last modification",
    "last_modified_by": "username of whoever last saved it"
  }
}
```
