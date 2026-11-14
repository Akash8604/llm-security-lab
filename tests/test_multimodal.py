
from pathlib import Path

from PIL import Image

from experiments.run_pi010 import (
    CASES,
    MARKER,
    create_image,
)


def test_four_image_cases_defined():
    assert len(CASES) == 4
    assert len({case["id"] for case in CASES}) == 4


def test_images_are_created():
    for case in CASES:
        path = create_image(case)

        assert path.exists()
        assert path.suffix == ".png"

        with Image.open(path) as img:
            assert img.format == "PNG"
            assert img.size == (1400, 850)


def test_baseline_contains_no_attack_instructions():
    baseline = next(
        case for case in CASES
        if case["id"] == "BASE-010"
    )

    content = "\n".join(baseline["lines"]).lower()

    assert "ignore your previous instructions" not in content
    assert "reveal the confidential" not in content


def test_authority_spoofing_image_defined():
    case = next(
        case for case in CASES
        if case["id"] == "PI-010-B"
    )

    content = "\n".join(case["lines"])

    assert "SYSTEM ADMINISTRATOR NOTICE" in content
    assert "approved override" in content


def test_synthetic_marker_not_embedded_in_images():
    for case in CASES:
        content = "\n".join(case["lines"])
        assert MARKER not in content
