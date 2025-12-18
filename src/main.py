"""
Application entrypoint.

Allows running the full Bitrix deal export pipeline
as a standalone script.

Future-friendly for packaging (PyInstaller / Nuitka).

To properly run this application, use the command below:
    $ python -m src.main
"""

from src.pipelines.deal_export_pipeline import run_export


def main() -> None:
    """
    Main execution entrypoint.
    """

    print("=== Bitrix Deal Export ===\n")

    # Fetch deals starting from the specified date (yyyy-mm-dd format).
    start_date = "2025-01-01"

    # Complete pipeline execution, from Bitrix24 API requests to export to Google Sheets.
    run_export(start_date=start_date)

    print("\n=== Execution finished ===")


if __name__ == "__main__":
    main()
