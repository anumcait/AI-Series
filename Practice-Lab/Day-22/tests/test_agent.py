"""Tests for the Day 22 DevOps agent."""

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agent import DevOpsAgent
from models import validate_action
from tools import (
    check_disk_usage,
    check_server_health,
    check_service_status,
)


def test_server_health():
    result = check_server_health()
    assert result["health"] == "HEALTHY"
    assert result["cpu_percent"] == 34


def test_disk_usage_warning():
    result = check_disk_usage()
    assert result["disk_percent"] == 87
    assert result["status"] == "WARNING"


def test_nginx_running():
    result = check_service_status("nginx")
    assert result["status"] == "RUNNING"


def test_unknown_service_is_rejected():
    result = check_service_status("unknown")
    assert "error" in result


def test_unknown_tool_is_rejected():
    valid, _ = validate_action({
        "tool": "delete_files",
        "arguments": {},
    })
    assert not valid


def test_invalid_service_argument_is_rejected():
    valid, _ = validate_action({
        "tool": "check_service_status",
        "arguments": {"service_name": "unknown"},
    })
    assert not valid


def test_invalid_arguments_are_rejected():
    valid, _ = validate_action({
        "tool": "check_disk_usage",
        "arguments": {"path": "C:\\"},
    })
    assert not valid


def test_empty_goal_is_rejected():
    agent = DevOpsAgent()
    with pytest.raises(ValueError):
        agent.run("  ")


def test_max_steps_must_be_positive():
    with pytest.raises(ValueError):
        DevOpsAgent(max_steps=0)


def test_agent_observes_tool_result_and_finishes():
    agent = DevOpsAgent(max_steps=3)

    tool_decision = {
        "type": "tool",
        "tool": "check_disk_usage",
        "arguments": {},
        "reason": "Check disk utilization.",
    }

    final_decision = {
        "type": "final",
        "answer": "Disk utilization is 87%; investigate disk consumption.",
    }

    responses = [
        SimpleNamespace(
            message=SimpleNamespace(
                content=json.dumps(tool_decision)
            )
        ),
        SimpleNamespace(
            message=SimpleNamespace(
                content=json.dumps(final_decision)
            )
        ),
    ]

    with patch("agent.ollama.chat", side_effect=responses) as mock_chat:
        result = agent.run("Check disk usage.")

    assert result["observations"][0]["result"]["disk_percent"] == 87
    assert "87%" in result["answer"]
    assert len(result["observations"]) == 1
    assert mock_chat.call_count == 2