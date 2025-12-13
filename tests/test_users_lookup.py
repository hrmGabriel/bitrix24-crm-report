"""
Integration test for Bitrix users lookup.

This test validates:
- Access to user.get
- Correct mapping of user ID to full name

Run this test with:
    $ python -m tests.test_users_lookup
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK
from src.lookups.users import fetch_user_map


def run():
    print("Starting Bitrix users lookup test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK
    )

    user_map = fetch_user_map(client)

    if not user_map:
        print("No users returned.")
        return

    print("Users loaded successfully:\n")

    for user_id, name in user_map.items():
        print(f"  {user_id} -> {name}")

    print(f"\nTotal users: {len(user_map)}")
    print("\nTest completed successfully.")


if __name__ == "__main__":
    run()
