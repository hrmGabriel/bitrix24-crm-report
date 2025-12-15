"""
Deal loader utilities.

Responsible for:
- Fetching deals from Bitrix24 CRM
- Handling pagination safely
- Returning raw deal data for further enrichment
"""

from typing import List, Dict, Any
from src.bitrix_client import BitrixClient


DEAL_SELECT_FIELDS = [
    "ID",
    "CATEGORY_ID",
    "STAGE_ID",
    "COMPANY_ID",
    "ASSIGNED_BY_ID",
    "TITLE",
    "TYPE_ID",
    "SOURCE_ID",
    "OPPORTUNITY",
    "DATE_CREATE",
    "BEGINDATE",
    "CLOSEDATE",
    "UF_CRM_1750948742478",   # Order description
    "UF_CRM_1750950619818",   # Consultant name
    "UF_CRM_1750951091402",   # Management
    "UF_CRM_1751306725382",   # Advanced sale type
    "UF_CRM_1751332724412",   # Total devices value
    "UF_CRM_1753968931293",   # Document type
]


def fetch_deals(
    client: BitrixClient,
    start_date: str | None = None
) -> List[Dict[str, Any]]:
    """
    Fetches CRM deals with optional date filtering.

    Args:
        start_date: ISO date string (YYYY-MM-DD).
                    If provided, only deals created on or after this date are fetched.
    """

    payload: Dict[str, Any] = {
        "select": ["*"]
    }

    if start_date:
        payload["filter"] = {
            ">=DATE_CREATE": start_date
        }

    return client.call_all("crm.deal.list", payload)
