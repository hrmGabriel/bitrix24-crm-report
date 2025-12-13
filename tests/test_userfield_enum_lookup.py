"""
Integration test for Bitrix24 userfield enum lookup.

This test validates:
- API connectivity via webhook
- Access to crm.deal.userfield.list
- Correct extraction of enum LIST values
- Dynamic mapping of enum ID -> label

This test uses real API calls.
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK
from src.lookups.userfield_enums import fetch_userfield_enum_map


def run():
    print("Starting Bitrix24 userfield enum lookup test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK
    )

    # Internal ID of the userfield "Gerência"
    USERFIELD_ID = 261

    enum_map = fetch_userfield_enum_map(
        client=client,
        userfield_id=USERFIELD_ID
    )

    if not enum_map:
        print("No enum values returned.")
        print("Check if the userfield ID is correct or if it has enum values.")
        return

    print("Enum values loaded successfully:\n")

    for enum_id, label in enum_map.items():
        print(f"  {enum_id} -> {label}")

    print(f"\nTotal enum values: {len(enum_map)}")
    print("\nTest completed successfully.")


if __name__ == "__main__":
    run()
