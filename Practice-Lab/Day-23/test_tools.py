from tools import (
    check_server_health,
    monitor_resources,
    check_services,
    analyze_logs,
    dispatch_tool,
    to_json,
)


def main():
    print("\n1. Server health")
    print(to_json(check_server_health()))

    print("\n2. Resource monitor")
    print(to_json(monitor_resources()))

    print("\n3. Service checker")
    print(to_json(check_services()))

    print("\n4. Resource logs")
    print(to_json(analyze_logs("resource")))

    print("\n5. Invalid tool")
    print(to_json(dispatch_tool("delete_server", {})))

    print("\n6. Invalid log category")
    print(to_json(dispatch_tool(
        "analyze_logs", {"category": "unknown"}
    )))


if __name__ == "__main__":
    main()