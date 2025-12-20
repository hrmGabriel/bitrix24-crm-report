"""
Company lookup utilities.

Responsible for:
- Fetching CRM companies by ID
- Building a lookup:
  { company_id: company_title }

This implementation avoids crm.company.list due to scalability and
pagination issues on large datasets.
"""

from typing import Dict, Iterable, List
from src.bitrix_client import BitrixClient


def _chunked(values: List[int], size: int):
    for i in range(0, len(values), size):
        yield values[i:i + size]


def fetch_company_map(
    client: BitrixClient,
    company_ids: Iterable[int],
) -> Dict[int, str]:
    """
    Fetches CRM companies by ID and builds a lookup map.

    This optimized implementation uses crm.company.list with
    batched ID filters to avoid N+1 requests and drastically
    improve performance on large datasets.

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
    unique_company_ids = sorted({cid for cid in company_ids if cid})
    total = len(unique_company_ids)

    if not unique_company_ids:
        return company_map

    # Bitrix safely supports 50 IDs per filter
    batches = list(_chunked(unique_company_ids, 50))
    total_batches = len(batches)

    print(f"Resolving companies... 0/{total}", end="", flush=True)

    resolved = 0

    for batch_index, id_batch in enumerate(batches, start=1):
        companies = client.call_all(
            "crm.company.list",
            payload={
                "filter": {
                    "ID": id_batch
                },
                "select": ["ID", "TITLE"],
            }
        )

        for company in companies:
            try:
                company_id = int(company["ID"])
                title = company.get("TITLE", "").strip()
            except (KeyError, ValueError):
                continue

            company_map[company_id] = title or "Unnamed Company"
            resolved += 1

        # Dynamic progress update (based on resolved companies)
        print(f"\rResolving companies... {resolved}/{total}", end="", flush=True)

    print()

    return company_map
