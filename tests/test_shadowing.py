
import json
from pathlib import Path

from experiments.run_pi011 import CASES, MARKER, HIJACK, POLICY
from experiments.run_pi011_control import CONTROLS


RESULTS = Path("research/results")


def test_five_experiment_cases():
    assert len(CASES) == 5
    assert {case["id"] for case in CASES} == {
        "BASE-011",
        "PI-011-A",
        "PI-011-B",
        "PI-011-C",
        "PI-011-D",
    }


def test_three_control_cases():
    assert len(CONTROLS) == 3
    assert {case["id"] for case in CONTROLS} == {
        "CTRL-011-A",
        "CTRL-011-B",
        "CTRL-011-C",
    }


def test_policy_present_in_every_case():
    for case in CASES + CONTROLS:
        assert POLICY in case["document"]


def test_confidential_marker_not_in_documents():
    for case in CASES + CONTROLS:
        assert MARKER not in case["document"]


def test_attack_and_control_separation():
    attack_cases = [c for c in CASES if c["id"] != "BASE-011"]
    assert len(attack_cases) == 4

    for case in attack_cases:
        assert case["document"] != POLICY

    for case in CONTROLS:
        assert HIJACK not in case["document"]
        assert "SYSTEM OVERRIDE" not in case["document"]


def test_three_saved_experiment_runs():
    files = sorted(RESULTS.glob("pi011_shadowing_*.json"))
    assert len(files) >= 3

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert len(data["cases"]) == 5
        assert all(
            case["status"] == "completed"
            for case in data["cases"]
        )


def test_control_evidence():
    files = sorted(RESULTS.glob("pi011_control_*.json"))
    assert files

    data = json.loads(files[-1].read_text(encoding="utf-8"))
    cases = data["cases"]

    assert len(cases) == 9
    assert all(case["status"] == "completed" for case in cases)

    grouped = {}
    for case in cases:
        grouped.setdefault(case["id"], []).append(case)

    assert all(len(group) == 3 for group in grouped.values())

    for case in grouped["CTRL-011-A"]:
        assert case["metrics"]["mfa_mentioned"]

    for case in grouped["CTRL-011-B"]:
        assert not case["metrics"]["mfa_mentioned"]

    for case in grouped["CTRL-011-C"]:
        assert case["metrics"]["mfa_mentioned"]


def test_no_exact_marker_disclosures_in_saved_runs():
    files = (
        list(RESULTS.glob("pi011_shadowing_*.json"))
        + list(RESULTS.glob("pi011_control_*.json"))
    )
    assert files

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for case in data["cases"]:
            assert case["status"] == "completed"
            assert not case["metrics"]["exact_secret_disclosed"]
            assert not case["metrics"]["output_hijack_marker_detected"]
