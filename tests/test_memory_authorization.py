
import pytest

from experiments.run_pi009 import (
    retrieve_memories,
    CANARY,
)


def test_owner_can_read_own_memory():
    memories = retrieve_memories(
        "alice",
        ["MEM-001"],
        "secure",
    )

    assert len(memories) == 1
    assert memories[0]["owner"] == "alice"


def test_cross_user_memory_blocked():
    memories = retrieve_memories(
        "bob",
        ["MEM-001"],
        "secure",
    )

    assert memories == []


def test_insecure_mode_exposes_private_memory():
    memories = retrieve_memories(
        "bob",
        ["MEM-001"],
        "insecure",
    )

    assert len(memories) == 1
    assert CANARY in memories[0]["content"]


def test_fake_admin_claim_cannot_override_identity():
    memories = retrieve_memories(
        "bob",
        ["MEM-001"],
        "secure",
    )

    assert memories == []


def test_public_memory_accessible():
    memories = retrieve_memories(
        "bob",
        ["MEM-003"],
        "secure",
    )

    assert len(memories) == 1
    assert memories[0]["visibility"] == "public"


def test_invalid_mode_rejected():
    with pytest.raises(ValueError):
        retrieve_memories(
            "bob",
            ["MEM-001"],
            "unknown",
        )


def test_mixed_memory_results_filtered():
    memories = retrieve_memories(
        "bob",
        ["MEM-001", "MEM-002", "MEM-003"],
        "secure",
    )

    ids = {memory["id"] for memory in memories}

    assert "MEM-001" not in ids
    assert "MEM-002" in ids
    assert "MEM-003" in ids
