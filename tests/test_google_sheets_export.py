"""
Google Sheets export integration test.

Validates:
- Authentication with Google Sheets API
- Data upload
- Column auto-resize

Run this test with:
    $ python -m tests.test_google_sheets_export
"""

from src.exporters.google_sheets_exporter import export_to_google_sheets
from src.config import GOOGLE_SHEET_ID


def run() -> None:
    print("Starting Google Sheets export test...\n")

    headers = [
        "Pipeline",
        "Stage",
        "Company",
        "Responsible",
        "Revenue",
        "Created At",
    ]

    rows = [
        [
            "Pré vendas",
            "Contato inicial",
            "ACME LTDA",
            "João Silva",
            "1500.00",
            "11/12/2025",
        ],
        [
            "Vendas",
            "Fechado",
            "Global Tech",
            "Maria Souza",
            "2999.90",
            "12/12/2025",
        ],
    ]

    export_to_google_sheets(
        spreadsheet_id=GOOGLE_SHEET_ID,
        sheet_name="Folha1",
        rows=rows,
        credentials_path="credentials.json",
        headers=headers,
    )

    print("Google Sheets export test completed successfully.")


if __name__ == "__main__":
    run()
