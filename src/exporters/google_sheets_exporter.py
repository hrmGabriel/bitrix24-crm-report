"""
Google Sheets exporter.

Responsibilities:
- Authenticate using a Google Service Account.
- Export tabular data to a Google Spreadsheet.
- Clear existing content before writing.
- Auto-resize columns for better readability.

This exporter always performs a full refresh:
- Clears the entire sheet.
- Rewrites headers and all rows.

This behavior is intentional to keep dashboards consistent.
"""

from typing import List
from googleapiclient.discovery import build
from google.oauth2 import service_account


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def export_to_google_sheets(
    spreadsheet_id: str,
    sheet_name: str,
    rows: List[List],
    credentials_path: str,
    headers: List[str] | None = None, # Optional
) -> None:
    """
    Exports data to a Google Sheet.

    Args:
        spreadsheet_id: Target Google Spreadsheet ID
        sheet_name: Sheet/tab name
        headers: Column headers
        rows: Table rows
        credentials_path: Path to service account credentials JSON
    """

    # Auto-generate headers from the first row if not provided
    if not headers:
        if not rows:
            raise ValueError("Cannot export empty dataset to Google Sheets")

        headers = list(rows[0].keys())


    # Authenticate
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES,
    )

    service = build(
        "sheets",
        "v4",
        credentials=credentials,
        cache_discovery=False,  # avoids cache issues in some environments
    )

    sheets_api = service.spreadsheets()

    # Prepare data
    values = [headers] + rows

    # Clear existing content
    clear_range = f"{sheet_name}!A:Z"

    sheets_api.values().clear(
        spreadsheetId=spreadsheet_id,
        range=clear_range,
        body={},
    ).execute()

    # Write new data
    write_range = f"{sheet_name}!A1"

    sheets_api.values().update(
        spreadsheetId=spreadsheet_id,
        range=write_range,
        valueInputOption="RAW",
        body={"values": values},
    ).execute()

    # Auto-resize columns
    sheet_metadata = sheets_api.get(
        spreadsheetId=spreadsheet_id
    ).execute()

    sheet_id = None
    for sheet in sheet_metadata["sheets"]:
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break

    if sheet_id is not None:
        requests = [
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": len(headers),
                    }
                }
            }
        ]

        sheets_api.batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ).execute()
