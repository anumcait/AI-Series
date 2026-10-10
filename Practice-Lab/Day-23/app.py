import json

from tools import (
    check_server_health,
    monitor_resources,
    check_services,
    analyze_logs,
    dispatch_tool,
    to_json,
)


def run_tool(tool_name, arguments=None):
    """Execute a registered tool and return its result."""
    arguments = arguments or {}

    try:
        result = dispatch_tool(tool_name, arguments)

        # Normalize the result so the agent can process it.
        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"result": result}

        return result

    except Exception as exc:
        return {
            "ok": False,
            "error": f"Tool execution failed: {exc}",
            "tool": tool_name,
        }


def needs_log_investigation(resource_result, service_result):
    """Decide whether the results justify inspecting logs."""
    resource_text = json.dumps(resource_result).lower()
    service_text = json.dumps(service_result).lower()

    warning_indicators = (
        "warning",
        "critical",
        "high",
        "failed",
        "unhealthy",
        "stopped",
        "error",
    )

    return any(
        indicator in resource_text or indicator in service_text
        for indicator in warning_indicators
    )


def investigate_server():
    """Coordinate the multi-tool server investigation."""
    report = {
        "investigation": "server_health",
        "steps": [],
    }

    print("\n=== Day 23: Multi-Tool DevOps Agent ===")
    print("\n[1/4] Checking server health...")

    health = run_tool("check_server_health")
    report["steps"].append({
        "tool": "check_server_health",
        "result": health,
    })
    print(to_json(health))

    print("\n[2/4] Monitoring CPU, memory, and disk...")

    resources = run_tool("monitor_resources")
    report["steps"].append({
        "tool": "monitor_resources",
        "result": resources,
    })
    print(to_json(resources))

    print("\n[3/4] Checking application services...")

    services = run_tool("check_services")
    report["steps"].append({
        "tool": "check_services",
        "result": services,
    })
    print(to_json(services))

    print("\n[4/4] Deciding whether log analysis is needed...")

    if needs_log_investigation(resources, services):
        print("A warning indicator was detected. Inspecting logs...")

        logs = run_tool(
            "analyze_logs",
            {"category": "all"},
        )

        report["steps"].append({
            "tool": "analyze_logs",
            "result": logs,
        })
        print(to_json(logs))
    else:
        print("No warning indicators detected. Log analysis skipped.")

    print("\n=== Consolidated Investigation Report ===")
    print(json.dumps(report, indent=2, default=str))

    return report


def main():
    investigate_server()


if __name__ == "__main__":
    main()