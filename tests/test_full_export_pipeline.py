"""
Full deal export pipeline integration test.

Validates:
- Deal loading
- Enrichment
- Normalization
- XLSX generation
"""

from src.pipelines.deal_export_pipeline import run_export


def run() -> None:
    print("Starting full export pipeline test...\n")

    # Fetch deals from the last 1 day
    run_export(days_back=1)

    print("\nFull export pipeline test completed.")


if __name__ == "__main__":
    run()
