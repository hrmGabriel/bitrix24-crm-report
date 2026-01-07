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
import time
import socket

from typing import List
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Maximum number of rows written per request to avoid Google API timeouts
# This prevents payload size and request duration issues
CHUNK_SIZE = 500

# Maximum retry attempts when hitting Google API rate limits (HTTP 429)
MAX_RETRIES = 5

# Delay (seconds) between write requests to respect Google Sheets API quotas
WRITE_DELAY_SECONDS = 1


def execute_with_retry(request):
    """
    Executes a Google API request with retry and exponential backoff.

    Handles:
    - HTTP 429 (rate limit)
    - Network / SSL timeouts
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return request.execute()
        except HttpError as e:
            if e.resp.status == 429 and attempt < MAX_RETRIES:
                sleep_time = attempt * 2
                time.sleep(sleep_time)
                continue
            raise
        except (TimeoutError, socket.timeout):
            # Network timeout — retry with backoff
            if attempt < MAX_RETRIES:
                sleep_time = attempt * 2
                time.sleep(sleep_time)
                continue
            raise


def export_to_google_sheets(
    spreadsheet_id: str,
    sheet_name: str,
    rows: List[List],
    credentials_path: str,
    headers: List[str] | None = None,  # Optional
) -> None:
    """
    Exports data to a Google Sheet.

    Args:
        spreadsheet_id: Target Google Spreadsheet ID
        sheet_name: Sheet/tab name
        headers: Column headers
        rows: Table rows (list of dictionaries)
        credentials_path: Path to service account credentials JSON
    """

    # Auto-generate headers from the first row if not provided
    if not headers:
        if not rows:
            raise ValueError("Cannot export empty dataset to Google Sheets")

        headers = list(rows[0].keys())

    # Authenticate using Google Service Account credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES,
    )

    service = build(
        "sheets",
        "v4",
        credentials=credentials,
        cache_discovery=False,  # Avoids cache issues in CI environments
    )

    sheets_api = service.spreadsheets()

    # Convert list of dicts into list of lists
    # Header is written separately to simplify chunking logic
    values = []
    for row in rows:
        values.append([row.get(header, "") for header in headers])

    # Clear existing content from the sheet
    clear_range = f"{sheet_name}!A:Z"

    execute_with_retry(
        sheets_api.values().clear(
            spreadsheetId=spreadsheet_id,
            range=clear_range,
            body={},
        )
    )

    # Write header row (single request)
    header_range = f"{sheet_name}!A1"

    execute_with_retry(
        sheets_api.values().update(
            spreadsheetId=spreadsheet_id,
            range=header_range,
            valueInputOption="RAW",
            body={"values": [headers]},
        )
    )

    # Small delay to avoid hitting write quota immediately
    time.sleep(WRITE_DELAY_SECONDS)

    # Write data rows in chunks to avoid request size and timeout issues
    start_row = 2  # Data starts after header row

    for i in range(0, len(values), CHUNK_SIZE):
        chunk = values[i : i + CHUNK_SIZE]

        write_range = f"{sheet_name}!A{start_row}"

        execute_with_retry(
            sheets_api.values().update(
                spreadsheetId=spreadsheet_id,
                range=write_range,
                valueInputOption="RAW",
                body={"values": chunk},
            )
        )

        start_row += len(chunk)

        # Delay between write requests to respect Google Sheets API rate limits
        time.sleep(WRITE_DELAY_SECONDS)

    # Retrieve sheet metadata to get internal sheet ID
    sheet_metadata = execute_with_retry(
        sheets_api.get(spreadsheetId=spreadsheet_id)
    )

    sheet_id = None
    for sheet in sheet_metadata["sheets"]:
        if sheet["properties"]["title"] == sheet_name:
            sheet_id = sheet["properties"]["sheetId"]
            break
    
    # Auto-resize columns for better readability
    # This step is optional and may timeout on large sheets
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

        try:
            execute_with_retry(
                sheets_api.batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": requests},
                )
            )
        except (TimeoutError, socket.timeout):
            # Non-fatal: data was already written successfully
            print(
                "Warning: column auto-resize timed out. "
                "Data export completed successfully."
            )

        execute_with_retry(
            sheets_api.batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests},
            )
        )
