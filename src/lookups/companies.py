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

    # Normalize and deduplicate company IDs
    unique_company_ids = [cid for cid in set(company_ids) if cid]
    total = len(unique_company_ids)

    print(f"Resolving companies... 0/{total}", end="", flush=True)

    for index, company_id in enumerate(unique_company_ids, start=1):
        try:
            response = client.call(
                "crm.company.get",
                payload={"id": company_id},
            )
        except Exception:
            # Non-fatal: deals may reference deleted companies
            print(f"\rResolving companies... {index}/{total}", end="", flush=True)
            continue

        company = response.get("result")
        if not company:
            print(f"\rResolving companies... {index}/{total}", end="", flush=True)
            continue

        title = company.get("TITLE", "").strip()
        if not title:
            title = "Unnamed Company"

        company_map[company_id] = title

        # Dynamic progress update
        print(f"\rResolving companies... {index}/{total}", end="", flush=True)

    print()  # Final line break after progress completion

    return company_map
