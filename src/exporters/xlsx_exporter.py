"""
XLSX exporter.

Responsible for:
- Writing normalized deal data to an Excel file
"""

from typing import List, Dict, Any
from openpyxl import Workbook


def export_deals_to_xlsx(
    deals: List[Dict[str, Any]],
    output_path: str,
) -> None:
    """
    Exports deals to an XLSX file.

    Args:
        deals: List of normalized deal dictionaries
        output_path: Path to output XLSX file
    """

    if not deals:
        raise ValueError("No deals provided for export")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Deals"

    headers = list(deals[0].keys())
    sheet.append(headers)

    for deal in deals:
        row = [deal.get(header, "") for header in headers]
        sheet.append(row)

    workbook.save(output_path)
