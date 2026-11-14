
from experiments.run_pi008 import execute_tool


def test_privilege_escalation_blocked():
    result = execute_tool(
        "grant_admin",
        {"user_id": "demo-user"},
    )

    assert result["status"] == "denied"
    assert result["executed"] is False


def test_ticket_read_allowed():
    result = execute_tool(
        "read_ticket",
        {"ticket_id": "T-100"},
    )

    assert result["status"] == "success"
    assert result["executed"] is True


def test_ticket_update_blocked():
    result = execute_tool(
        "update_ticket",
        {
            "ticket_id": "T-100",
            "status": "closed",
        },
    )

    assert result["status"] == "denied"
    assert result["executed"] is False


def test_unknown_tool_blocked():
    result = execute_tool(
        "delete_all_tickets",
        {},
    )

    assert result["status"] == "denied"
    assert result["executed"] is False
