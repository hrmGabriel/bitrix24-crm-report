"""
Company lookup utilities.

Responsible for:
- Fetching CRM companies by ID
- Building a lookup:
  { company_id: company_title }

This implementation avoids crm.company.list due to scalability and
pagination issues on large datasets.
"""

from typing import Dict, Iterable
from src.bitrix_client import BitrixClient


def fetch_company_map(
        client: BitrixClient,
        company_ids: Iterable[int],
    ) -> Dict[int, str]:
    """
    Fetches CRM companies by ID and builds a lookup map.

    This function uses crm.company.get to avoid loading the entire
    company database, which may contain tens of thousands of records.

    Args:
        client: Initialized BitrixClient
        company_ids: Iterable of company IDs referenced by deals

    Returns:
        {
            184: "ACME Telecom LTDA",
            231: "Global Networks SA"
        }
    """

    company_map: Dict[int, str] = {}

    for company_id in set(company_ids):
        # Skip invalid or empty IDs
        if not company_id:
            continue

        try:
            response = client.call(
                "crm.company.get",
                payload={"id": company_id},
            )
        except Exception:
            # Non-fatal: deals may reference deleted companies
            continue

        company = response.get("result")
        if not company:
            continue

        title = company.get("TITLE", "").strip()
        if not title:
            title = "Unnamed Company"

        company_map[company_id] = title

    return company_map
