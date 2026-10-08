def calculate(expression: str):
    """
    Calculate a mathematical expression.
    """

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return {
            "expression": expression,
            "result": result
        }

    except Exception as e:
        return {
            "expression": expression,
            "error": str(e)
        }


def get_server_status(server: str):
    """
    Get the status of a server.
    """

    servers = {
        "production": "HEALTHY",
        "test": "WARNING",
        "development": "HEALTHY"
    }

    status = servers.get(
        server.lower(),
        "UNKNOWN"
    )

    return {
        "server": server,
        "status": status
    }


def get_disk_usage(server: str):
    """
    Get disk usage of a server.
    """

    disk_usage = {
        "production": 78,
        "test": 91,
        "development": 45
    }

    usage = disk_usage.get(
        server.lower()
    )

    if usage is None:
        return {
            "server": server,
            "error": "Server not found"
        }

    return {
        "server": server,
        "disk_usage_percent": usage
    }


def check_service(server: str, service: str):
    """
    Check the status of a service on a server.
    """

    services = {
        "production": {
            "tomcat": "RUNNING",
            "nginx": "RUNNING",
            "oracle": "RUNNING"
        },

        "test": {
            "tomcat": "RUNNING",
            "nginx": "STOPPED",
            "oracle": "RUNNING"
        },

        "development": {
            "tomcat": "RUNNING",
            "nginx": "RUNNING",
            "oracle": "STOPPED"
        }
    }

    server_services = services.get(
        server.lower()
    )

    if server_services is None:
        return {
            "server": server,
            "service": service,
            "error": "Server not found"
        }

    status = server_services.get(
        service.lower(),
        "UNKNOWN"
    )

    return {
        "server": server,
        "service": service,
        "status": status
    }