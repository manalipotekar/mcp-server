# system_tools.py
"""
System automation tools for MCP:
- open system settings
- set brightness
"""

import platform
import subprocess
from mcp.server.fastmcp import FastMCP

# Create a separate MCP instance for modularity
mcp = FastMCP("SystemTools")

def run_cmd(cmd_list):
    """Run command safely and return success, stdout, stderr."""
    try:
        proc = subprocess.run(cmd_list, capture_output=True, text=True, check=True)
        return True, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stdout.strip() if e.stdout else "", e.stderr.strip() or str(e)

def clamp_percent(p):
    try:
        p = int(p)
    except Exception:
        raise ValueError("percent must be an integer 0–100")
    return max(0, min(100, p))


@mcp.tool()
def open_settings() -> str:
    """Open system settings or control panel."""
    osname = platform.system()
    if osname == "Windows":
        run_cmd(["powershell", "-NoProfile", "-Command", "Start-Process ms-settings:"])
        return "Opened Windows Settings."
    elif osname == "Darwin":
        run_cmd(["osascript", "-e", 'tell application "System Settings" to activate'])
        return "Opened macOS System Settings."
    elif osname == "Linux":
        for cmd in (["gnome-control-center"], ["systemsettings5"], ["xdg-open", "settings://"]):
            ok, _, _ = run_cmd(cmd)
            if ok:
                return "Opened Linux system settings."
        return "Failed to open system settings."
    return f"Unsupported OS: {osname}"


@mcp.tool()
def set_brightness(percent: int) -> str:
    """Set display brightness (best-effort per OS)."""
    p = clamp_percent(percent)
    osname = platform.system()

    if osname == "Windows":
        ps = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{p})"
        ok, _, err = run_cmd(["powershell", "-NoProfile", "-Command", ps])
        return f"{'Success' if ok else 'Failed'} to set brightness on Windows. {err or ''}"

    if osname == "Darwin":
        val = f"{p/100:.3f}"
        for path in ["/usr/local/bin/brightness", "/opt/homebrew/bin/brightness"]:
            ok, _, _ = run_cmd([path, val])
            if ok:
                return f"Set brightness to {p}% on macOS."
        return "Install 'brightness' via Homebrew to enable brightness control."

    if osname == "Linux":
        ok, _, _ = run_cmd(["brightnessctl", "set", f"{p}%"])
        if ok:
            return f"Set brightness to {p}% using brightnessctl."
        return "brightnessctl not found or failed."

    return f"Unsupported OS: {osname}"
