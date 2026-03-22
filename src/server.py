"""MCP server"""

from mcp.server.fastmcp import FastMCP

from src.settings import mcp_run_settings, mcp_server_settings
from src.tools import adding_content, creating, editing, reading

mcp = FastMCP(
    name="docx-mcp-server",
    host=mcp_server_settings.host,
    port=mcp_server_settings.port,
)

mcp.tool()(reading.read_docx)
mcp.tool()(reading.get_document_info)
mcp.tool()(reading.list_paragraphs)
mcp.tool()(reading.read_table)
mcp.tool()(reading.list_styles)
mcp.tool()(creating.create_docx)
mcp.tool()(adding_content.add_paragraph)
mcp.tool()(adding_content.add_heading)
mcp.tool()(adding_content.add_table)
mcp.tool()(adding_content.add_picture)
mcp.tool()(adding_content.add_page_break)
mcp.tool()(editing.find_replace)
mcp.tool()(editing.update_paragraph)
mcp.tool()(editing.delete_paragraph)
mcp.tool()(editing.set_core_properties)
mcp.tool()(editing.merge_documents)

if __name__ == "__main__":
    mcp.run(transport=mcp_run_settings.transport)
