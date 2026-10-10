"""
tools.py

Four independent, read-only diagnostic tools.
All values and log entries are simulated.
"""

import json
from typing import Any

from models import SERVER


def check_server_health() -> dict[str, Any]:
    """Check whether the simulated server is reachable.

    Returns:
        A dictionary containing the server name and availability.
    """
    return {
        "tool": "check_server_health",
        "server": SERVER.server_name,
        "reachable": SERVER.reachable,
        "status": "available" if SERVER.reachable else "unreachable",
    }


def monitor_resources() -> dict[str, Any]:
    """Check simulated CPU, memory, and disk utilization.

    Returns:
        Resource percentages and warning flags.
    """
    return {
        "tool": "monitor_resources",
        "server": SERVER.server_name,
        "cpu_percent": SERVER.cpu_percent,
        "memory_percent": SERVER.memory_percent,
        "disk_percent": SERVER.disk_percent,
        "warnings": {
            "cpu": SERVER.cpu_percent >= 80.0,
            "memory": SERVER.memory_percent >= 85.0,
            "disk": SERVER.disk_percent >= 85.0,
        },
    }


def check_services() -> dict[str, Any]:
    """Check the simulated Nginx, Tomcat, and database services.

    Returns:
        The status of each service.
    """
    return {
        "tool": "check_services",
        "server": SERVER.server_name,
        "services": dict(SERVER.services),
        "failed_services": [
            name
            for name, status in SERVER.services.items()
            if status.lower() != "running"
        ],
    }


def analyze_logs(category: str = "all") -> dict[str, Any]:
    """Inspect simulated log entries for resource or service issues.

    Args:
        category: One of 'all', 'resource', or 'service'.

    Returns:
        Matching simulated log entries.
    """
    category = category.strip().lower()

    if category not in {"all", "resource", "service"}:
        raise ValueError(
            "Invalid category. Use 'all', 'resource', or 'service'."
        )

    simulated_logs = [
        {
            "category": "resource",
            "level": "WARNING",
            "message": "Disk utilization reached 92%; "
                       "temporary files may require cleanup.",
        },
        {
            "category": "service",
            "level": "INFO",
            "message": "Nginx health check completed successfully.",
        },
        {
            "category": "service",
            "level": "INFO",
            "message": "Tomcat health check completed successfully.",
        },
        {
            "category": "service",
            "level": "INFO",
            "message": "Database health check completed successfully.",
        },
    ]

    matching_logs = [
        entry
        for entry in simulated_logs
        if category == "all" or entry["category"] == category
    ]

    return {
        "tool": "analyze_logs",
        "category": category,
        "entries_found": len(matching_logs),
        "entries": matching_logs,
        "note": "These are simulated log entries, not real server logs.",
    }


def dispatch_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """Validate and execute one registered tool."""

    registry = {
        "check_server_health": check_server_health,
        "monitor_resources": monitor_resources,
        "check_services": check_services,
        "analyze_logs": analyze_logs,
    }

    if tool_name not in registry:
        return {
            "ok": False,
            "error": f"Unknown tool: {tool_name}",
        }

    if not isinstance(arguments, dict):
        return {
            "ok": False,
            "error": "Tool arguments must be a JSON object.",
        }

    # Validate arguments before calling a function.
    if tool_name in {
        "check_server_health",
        "monitor_resources",
        "check_services",
    } and arguments:
        return {
            "ok": False,
            "error": f"{tool_name} does not accept arguments.",
        }

    if tool_name == "analyze_logs":
        if set(arguments) - {"category"}:
            return {
                "ok": False,
                "error": "analyze_logs accepts only 'category'.",
            }

        if "category" in arguments:
            if not isinstance(arguments["category"], str):
                return {
                    "ok": False,
                    "error": "'category' must be a string.",
                }

    try:
        result = registry[tool_name](**arguments)
        return {"ok": True, "data": result}

    except (TypeError, ValueError) as exc:
        return {
            "ok": False,
            "error": str(exc),
        }


def to_json(data: Any) -> str:
    """Serialize results for the LLM and the command line."""
    return json.dumps(data, ensure_ascii=False, indent=2)