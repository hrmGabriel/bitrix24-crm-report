"""
Status lookup integration test.

Validates:
- Fetching CRM statuses filtered by ENTITY_ID
- Proper mapping of STATUS_ID -> NAME

Common use case:
- Resolving SOURCE_ID values in crm.deal.list

Run this test with:
    $ python -m tests.test_status_lookup
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK
from src.lookups.statuses import fetch_status_map


# ENTITY_ID example:
# "SOURCE" -> deal source (WEBFORM, CALL, etc.)
ENTITY_ID = "SOURCE"


def run() -> None:
    print("Starting Bitrix24 status lookup test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK,
    )

    status_map = fetch_status_map(
        client=client,
        entity_id=ENTITY_ID,
    )

    print(f"Total statuses found for ENTITY_ID='{ENTITY_ID}': {len(status_map)}\n")

    # Print all statuses (usually a small list)
    for status_id, name in status_map.items():
        print(f"{status_id} -> {name}")

    if not status_map:
        raise RuntimeError("Status lookup returned an empty result.")

    print("\nStatus lookup test completed successfully.")


if __name__ == "__main__":
    run()
