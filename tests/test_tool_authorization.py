
from experiments.run_pi006 import execute_mock_tool


def test_unauthorized_transfer_blocked():
    result = execute_mock_tool(
        "transfer_funds",
        {
            "destination": "DEMO-ATTACKER",
            "amount": 500,
        },
    )

    assert result["status"] == "denied"
    assert result["executed"] is False


def test_authorized_balance_lookup():
    result = execute_mock_tool(
        "check_balance",
        {"account": "DEMO-001"},
    )

    assert result["status"] == "success"
    assert result["balance"] == 1000


def test_unknown_tool_blocked():
    result = execute_mock_tool(
        "unknown_function",
        {},
    )

    assert result["status"] == "denied"
    assert result["executed"] is False
