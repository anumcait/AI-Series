"""Simulated DevOps tools. No real servers are accessed."""

from typing import Any


SIMULATED_SERVER = {
    "server_name": "prod-web-01",
    "health": "HEALTHY",
    "cpu_percent": 34,
    "memory_percent": 62,
    "disk_percent": 87,
    "services": {
        "nginx": "RUNNING",
        "docker": "RUNNING",
    },
}


def check_server_health() -> dict[str, Any]:
    """Return simulated server health metrics."""
    return {
        "server_name": SIMULATED_SERVER["server_name"],
        "health": SIMULATED_SERVER["health"],
        "cpu_percent": SIMULATED_SERVER["cpu_percent"],
        "memory_percent": SIMULATED_SERVER["memory_percent"],
    }


def check_disk_usage() -> dict[str, Any]:
    """Return simulated disk utilization."""
    usage = SIMULATED_SERVER["disk_percent"]

    if usage >= 90:
        status = "CRITICAL"
    elif usage >= 80:
        status = "WARNING"
    else:
        status = "HEALTHY"

    return {
        "server_name": SIMULATED_SERVER["server_name"],
        "disk_percent": usage,
        "status": status,
        "recommendation": (
            "Investigate disk consumption and monitor free space."
            if status != "HEALTHY"
            else "Disk usage is within the normal range."
        ),
    }


def check_service_status(
    service_name: str = "nginx",
) -> dict[str, Any]:
    """Return the simulated status of an approved service."""
    service_name = service_name.lower()

    if service_name not in SIMULATED_SERVER["services"]:
        return {
            "error": f"Unknown simulated service: {service_name}",
            "allowed_services": list(
                SIMULATED_SERVER["services"].keys()
            ),
        }

    return {
        "server_name": SIMULATED_SERVER["server_name"],
        "service": service_name,
        "status": SIMULATED_SERVER["services"][service_name],
    }


def get_tool_registry() -> dict[str, Any]:
    """Return the tools available to the agent."""
    return {
        "check_server_health": check_server_health,
        "check_disk_usage": check_disk_usage,
        "check_service_status": check_service_status,
    }