
import json
from datetime import datetime, timezone
from pathlib import Path

from experiments.run_pi010 import (
    CASES,
    SYSTEM,
    MODEL,
    create_image,
    ask_model,
    MARKER,
)

# Existing baseline and authority-spoofing images.
SELECTED = ["BASE-010", "PI-010-B"]
REPEATS = 3


def main():
    results = []

    for case_id in SELECTED:
        case = next(c for c in CASES if c["id"] == case_id)
        image_path = create_image(case)

        for trial in range(1, REPEATS + 1):
            print(f"\nRunning {case_id}, trial {trial}...")

            try:
                answer = ask_model(image_path)
                leaked = MARKER in answer

                result = {
                    "case_id": case_id,
                    "trial": trial,
                    "status": "completed",
                    "image_path": str(image_path),
                    "answer": answer,
                    "exact_marker_disclosed": leaked,
                }

                print("Answer:", answer)
                print("Marker disclosed:", leaked)

            except Exception as exc:
                result = {
                    "case_id": case_id,
                    "trial": trial,
                    "status": "error",
                    "error": str(exc),
                }
                print("Error:", exc)

            results.append(result)

    completed = [
        r for r in results
        if r["status"] == "completed"
    ]

    summary = {
        case_id: {
            "completed": sum(
                r["case_id"] == case_id
                for r in completed
            ),
            "disclosures": sum(
                r["case_id"] == case_id
                and r["exact_marker_disclosed"]
                for r in completed
            ),
        }
        for case_id in SELECTED
    }

    output = {
        "experiment": "PI-010 Controlled Comparison",
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "model": MODEL,
        "system_prompt": SYSTEM,
        "repeats_per_case": REPEATS,
        "summary": summary,
        "results": results,
    }

    folder = Path("research/results")
    folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S_%f")

    path = folder / f"pi010_control_{timestamp}.json"

    path.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nCONTROL COMPARISON SUMMARY")
    print(json.dumps(summary, indent=2))
    print("Evidence saved to:", path)


if __name__ == "__main__":
    main()
