"""
User lookup utilities.

Responsible for:
- Fetching Bitrix users
- Building a lookup:
  { user_id: full_name }
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_user_map(client: BitrixClient) -> Dict[int, str]:
    """
    Fetches all Bitrix users and builds a lookup map.

    Returns:
        {
            41: "Ivete Lemos",
            9: "Admin"
        }
    """

    # This endpoint is paginated according to Bitrix API docs, which is handled by call_all
    users = client.call_all("user.get")

    if not users:
        return {}

    user_map: Dict[int, str] = {}

    for user in users:
        try:
            user_id = int(user["ID"])
        except (KeyError, ValueError):
            continue

        first_name = user.get("NAME", "").strip()
        last_name = user.get("LAST_NAME", "").strip()

        full_name = f"{first_name} {last_name}".strip()

        if not full_name:
            full_name = "Unknown User"

        user_map[user_id] = full_name

    return user_map
