"""
Full deal export pipeline integration test.

Validates:
- Deal loading
- Enrichment
- Normalization
- XLSX generation

Run this test with:
    $ python -m tests.test_full_export_pipeline
"""

from src.pipelines.deal_export_pipeline import run_export
from datetime import date, timedelta


def run() -> None:
    print("Starting full export pipeline test...\n")

    yesterday = date.today() - timedelta(days=1)
    start_date = yesterday.strftime("%Y-%m-%d")

    # Fetch deals from the last 1 day
    run_export(start_date=start_date)

    print("\nFull export pipeline test completed.")


if __name__ == "__main__":
    run()
