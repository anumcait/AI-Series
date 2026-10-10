"""
models.py

Centralized simulated server data and health thresholds.
No real server is accessed.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ServerSnapshot:
    server_name: str
    reachable: bool
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    services: dict[str, str]


# Illustrative test data. Change these values to test
# different investigation paths.
SERVER = ServerSnapshot(
    server_name="app-server-01",
    reachable=True,
    cpu_percent=41.0,
    memory_percent=68.0,
    disk_percent=92.0,
    services={
        "nginx": "running",
        "tomcat": "running",
        "database": "running",
    },
)

# Thresholds used by deterministic Python rules.
CPU_WARNING = 80.0
MEMORY_WARNING = 85.0
DISK_WARNING = 85.0

# A tool-call budget prevents excessive LLM-driven execution.
MAX_TOOL_CALLS = 6