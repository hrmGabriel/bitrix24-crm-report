"""
Company lookup utilities.

Responsible for:
- Fetching CRM companies
- Building a lookup:
  { company_id: company_title }
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_company_map(client: BitrixClient) -> Dict[int, str]:
    """
    Fetches all CRM companies and builds a lookup map.

    Returns:
        {
            184: "ACME Telecom LTDA",
            231: "Global Networks SA"
        }
    """

    # This endpoint is paginated according to Bitrix API docs, which is handled by call_all
    companies = client.call_all(
        "crm.company.list",
        payload={
            "select": ["ID", "TITLE"]
        }
    )

    if not companies:
        # Not fatal: some CRMs legitimately have no companies
        return {}

    company_map: Dict[int, str] = {}

    for company in companies:
        try:
            company_id = int(company["ID"])
        except (KeyError, ValueError):
            continue

        title = company.get("TITLE", "").strip()

        if not title:
            title = "Unnamed Company"

        company_map[company_id] = title

    return company_map
