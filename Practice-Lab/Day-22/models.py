"""Tool definitions and validation for the DevOps agent."""

from typing import Any

TOOL_SCHEMAS = {
    "check_server_health": {
        "description": "Check simulated server health and CPU/memory usage.",
        "parameters": {},
    },
    "check_disk_usage": {
        "description": "Check simulated server disk utilization.",
        "parameters": {},
    },
    "check_service_status": {
        "description": "Check a simulated service. Allowed: nginx, docker.",
        "parameters": {
            "service_name": {
                "type": "string",
                "allowed": ["nginx", "docker"],
            }
        },
    },
}


def validate_action(action: Any) -> tuple[bool, str]:
    """Validate a model-generated action before execution."""
    if not isinstance(action, dict):
        return False, "Action must be a JSON object."

    tool_name = action.get("tool")
    arguments = action.get("arguments", {})

    if tool_name not in TOOL_SCHEMAS:
        return False, f"Unknown tool: {tool_name!r}"

    if not isinstance(arguments, dict):
        return False, "Tool arguments must be a JSON object."

    schema = TOOL_SCHEMAS[tool_name]
    allowed_parameters = schema["parameters"]

    unexpected = set(arguments) - set(allowed_parameters)
    if unexpected:
        return False, f"Unexpected arguments: {sorted(unexpected)}"

    if tool_name == "check_service_status":
        service = arguments.get("service_name", "nginx")
        if service not in ("nginx", "docker"):
            return False, f"Service is not allowed: {service!r}"

    return True, "Valid action."