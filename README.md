# Docx MCP Server

An MCP server that exposes tools for reading, creating, and editing Microsoft Word (`.docx`) files. Built with the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and [python-docx](https://python-docx.readthedocs.io/).

## Running the Server

```bash
make project-init
cp .env.example .env
uv run --env-file .env python src/server.py
```

---

## Cline Configuration

Add this block to your `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "docx-mcp-server": {
      "command": "uv",
      "args": ["run", "src/server.py"],
      "type": "stdio",
      "cwd": "path/to/docx-mcp-server"
    }
  }
}
```

---

## Available Tools

### Reading

| Tool | Description |
|---|---|
| `read_docx(path)` | Extract all text from a document |
| `get_document_info(path)` | Metadata: paragraph count, tables, core properties |
| `list_paragraphs(path, start?, end?)` | List paragraphs with index, style and text |
| `read_table(path, table_index?)` | Extract a table as a 2-D array |
| `list_styles(path)` | All styles defined in the document, grouped by type |

### Creating

| Tool | Description |
|---|---|
| `create_docx(path, title?, author?, overwrite?)` | Create a new empty document |

### Adding Content

| Tool | Description |
|---|---|
| `add_paragraph(path, text, style?, bold?, italic?, font_size?, alignment?)` | Append a paragraph |
| `add_heading(path, text, level?)` | Append a heading (level 1–6) |
| `add_table(path, data, has_header_row?, style?)` | Append a table from a 2-D list |
| `add_picture(path, image_path, width_inches?)` | Embed an image |
| `add_page_break(path)` | Append a page break |

### Editing

| Tool | Description |
|---|---|
| `find_replace(path, find, replace, case_sensitive?)` | Global find-and-replace across paragraphs and tables |
| `update_paragraph(path, index, text?, style?, bold?, italic?, alignment?)` | Edit a paragraph by index |
| `delete_paragraph(path, index)` | Remove a paragraph by index |
| `set_core_properties(path, title?, author?, subject?, keywords?, comments?)` | Update document metadata |
| `merge_documents(base_path, other_path, output_path, add_page_break_between?)` | Merge two documents into one |


## Tests
### To run tests use
```bash
make project-init-dev

make run-tests
make run-tests -- -s
make run-tests -- -k get_document -vs
```
