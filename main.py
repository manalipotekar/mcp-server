"""
FastMCP quickstart example with note-making tools.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional
from datetime import datetime
from system_tools import open_settings, set_brightness


# Create an MCP server
mcp = FastMCP("Demo")
mcp.tool()(open_settings)
mcp.tool()(set_brightness)

# In-memory note storage
notes = {}


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Note-making tools
@mcp.tool()
def create_note(title: str, content: str, tags: Optional[str] = None) -> dict:
    """Create a new note with optional tags"""
    note_id = len(notes) + 1
    note = {
        "id": note_id,
        "title": title,
        "content": content,
        "tags": tags.split(",") if tags else [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    notes[note_id] = note
    return {"success": True, "note": note}


@mcp.tool()
def update_note(note_id: int, title: Optional[str] = None, content: Optional[str] = None, tags: Optional[str] = None) -> dict:
    """Update an existing note"""
    if note_id not in notes:
        return {"success": False, "error": f"Note {note_id} not found"}
    
    note = notes[note_id]
    if title is not None:
        note["title"] = title
    if content is not None:
        note["content"] = content
    if tags is not None:
        note["tags"] = tags.split(",")
    
    note["updated_at"] = datetime.now().isoformat()
    return {"success": True, "note": note}


@mcp.tool()
def delete_note(note_id: int) -> dict:
    """Delete a note by ID"""
    if note_id not in notes:
        return {"success": False, "error": f"Note {note_id} not found"}
    
    deleted_note = notes.pop(note_id)
    return {"success": True, "message": f"Note '{deleted_note['title']}' deleted"}


@mcp.tool()
def get_note(note_id: int) -> dict:
    """Retrieve a note by ID"""
    if note_id not in notes:
        return {"success": False, "error": f"Note {note_id} not found"}
    
    return {"success": True, "note": notes[note_id]}


@mcp.tool()
def list_notes(tag: Optional[str] = None) -> dict:
    """List all notes, optionally filtered by tag"""
    all_notes = list(notes.values())
    
    if tag:
        filtered_notes = [note for note in all_notes if tag in note["tags"]]
        return {"success": True, "notes": filtered_notes, "count": len(filtered_notes)}
    
    return {"success": True, "notes": all_notes, "count": len(all_notes)}


@mcp.tool()
def search_notes(query: str) -> dict:
    """Search notes by title or content"""
    query_lower = query.lower()
    results = [
        note for note in notes.values()
        if query_lower in note["title"].lower() or query_lower in note["content"].lower()
    ]
    return {"success": True, "results": results, "count": len(results)}

