"""
Company lookup integration test.

Validates:
- Connection with Bitrix24
- crm.company.get behavior
- Proper mapping of COMPANY_ID -> COMPANY_TITLE
- Resilience to invalid or missing company IDs
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK
from src.lookups.companies import fetch_company_map


def run() -> None:
    print("Starting Bitrix24 companies lookup test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK,
    )

    # Simulated company IDs (normally extracted from crm.deal.list)
    company_ids = [
        105,
        107,
        109,
        99999999,  # Invalid ID (should be safely ignored)
    ]

    company_map = fetch_company_map(
        client=client,
        company_ids=company_ids,
    )

    print(f"Companies resolved: {len(company_map)}\n")

    for company_id, company_name in company_map.items():
        print(f"- {company_id}: {company_name}")


if __name__ == "__main__":
    run()
