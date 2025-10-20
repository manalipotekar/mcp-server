# 🧠 MCP Server – Setup Guide

This guide walks you through setting up and connecting your custom **MCP server** (for example, a Leave Management or System Automation Server) with **Claude Desktop**.

---

## 🚀 Setup Steps

### 1. Install Claude Desktop  
Download and install **Claude Desktop** from [Anthropic’s official site](https://claude.ai).

---

### 2. Install `uv`  
Run the following command in your terminal to install [uv](https://docs.astral.sh/uv/):

```bash
pip install uv
```

---

### 3. Initialize a New MCP Server Project
Create a new project directory using:

```bash
uv init my-first-mcp-server
```

---

### 4. Add MCP CLI to Your Project
Inside the project directory, run:

```bash
uv add "mcp[cli]"
```

💡 This installs the MCP CLI so you can register and manage servers with Claude.

---

### 5. (Optional) Fix Type Errors
If you encounter type errors related to typer, upgrade it using:

```bash
pip install --upgrade typer
```

---

### 6. Write Your MCP Server Code
Edit the main.py file and implement your logic —
for example, a Leave Management Server that handles requests for leave approvals, or a System Automation Server that can perform actions like adjusting brightness or opening settings.

Example main.py structure:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def set_brightness(percent: int) -> str:
    """Set screen brightness to a specific percentage."""
    # Example: OS-specific brightness logic goes here
    return f"Brightness set to {percent}%"

@mcp.tool()
def open_settings() -> str:
    """Open system settings."""
    # Example: open settings using platform module
    return "Settings opened successfully"

if __name__ == "__main__":
    mcp.run()
```

---

### 7. Install the Server into Claude Desktop
From your project directory, run:

```bash
uv run mcp install main.py
```

🧩 This command registers your server with Claude so its tools become available inside the app.

---

### 8. Restart Claude Desktop
Kill any running instance of Claude from Task Manager, then relaunch Claude Desktop.

---

### 9. Verify Installation
Open Claude Desktop — you should now see tools provided by your MCP server listed in the interface.

---

## 💬 Example Prompts
Here are some example natural-language prompts you can use inside Claude Desktop once your MCP server is installed.

### 🖥️ System Automation Server
- "Increase my screen brightness to 80 percent."
- "Set brightness to 50%."
- "Open system settings."
- "Turn down the brightness to 30%."
- "Can you check and adjust the display brightness for me?"

### 🧳 Leave Management Server
- "Apply for 2 days of leave starting tomorrow."
- "Show me my remaining leave balance."
- "Cancel my last leave request."
- "List all approved leaves for this month."

---

## ✅ You're All Set!
Your MCP server is now installed and integrated with Claude.
You can start using its tools directly through natural language prompts inside Claude Desktop.

---

## 🧩 Optional Tips
- Use `uv run main.py` to test your server standalone before installing it.
- To uninstall or reinstall, re-run `uv run mcp install main.py`.
- You can create multiple MCP servers for different automation domains (e.g., media control, productivity, system tools).