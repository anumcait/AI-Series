
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Day31 Local Assistant")
ROOT = Path(os.environ["PROJECT_ROOT"]).resolve()

ALLOWED = {".txt", ".md", ".py", ".json", ".csv", ".yaml", ".yml"}


def safe_path(relative_path: str) -> Path:
    target = ROOT / relative_path

    # Reject symlinks before resolving the path.
    current = ROOT
    for part in Path(relative_path).parts:
        if part in (".", ".."):
            raise ValueError("Invalid relative path.")
        current = current / part
        if current.is_symlink():
            raise ValueError("Symbolic links are not allowed.")

    target = target.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("Access denied outside workspace.")
    return target


@mcp.tool()
def list_files() -> dict:
    """List supported files in the approved workspace."""
    files = []
    for path in ROOT.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        try:
            if not path.resolve().is_relative_to(ROOT):
                continue
            if path.suffix.lower() in ALLOWED:
                files.append(path.relative_to(ROOT).as_posix())
        except (OSError, ValueError):
            continue
    return {"files": sorted(files)}


@mcp.tool()
def read_file(path: str) -> dict:
    """Read a supported text file using a workspace-relative path."""
    target = safe_path(path)

    if not target.is_file():
        raise ValueError("File does not exist.")
    if target.suffix.lower() not in ALLOWED:
        raise ValueError("File type is not allowed.")
    if target.stat().st_size > 100_000:
        raise ValueError("File exceeds the 100 KB limit.")

    content = target.read_text(encoding="utf-8")
    return {
        "path": target.relative_to(ROOT).as_posix(),
        "content": content[:20_000],
        "truncated": len(content) > 20_000,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
