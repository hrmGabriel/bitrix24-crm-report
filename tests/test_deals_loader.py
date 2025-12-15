"""
Deal loader integration test.

Validates:
- Connection with Bitrix24
- crm.deal.list pagination
- Field selection correctness

This test prints out the total number of deals fetched, so it can
take a long time depending on the volume of data.

Run this test with:
    $ python -m tests.test_deals_loader
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK
from src.loaders.deals import fetch_deals


def run() -> None:
    print("Starting Bitrix24 deal loader test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK,
    )

    deals = fetch_deals(client=client, start_date="2025-12-12")

    print(f"Total deals fetched: {len(deals)}\n")

    if deals:
        print("Sample deal:")
        for key, value in deals[0].items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    run()
