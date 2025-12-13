"""
Userfield enum lookup utilities.

Responsible for:
- Fetching a deal userfield by internal ID
- Building a lookup from LIST:
  { list_item_id: value }
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_userfield_enum_map(
    client: BitrixClient,
    userfield_id: int
) -> Dict[str, str]:
    """
    Fetches a CRM deal userfield and builds a lookup map
    from its LIST attribute.

    Args:
        userfield_id: internal ID of the userfield

    Returns:
        {
            "427": "Inside Sales",
            "79": "Giovanny"
        }
    """

    response = client.call(
        "crm.deal.userfield.get",
        payload={"id": userfield_id}
    )

    result = response.get("result")

    if not result:
        raise RuntimeError(
            f"Userfield id={userfield_id} not found."
        )

    enum_list = result.get("LIST")

    if not enum_list:
        raise RuntimeError(
            f"Userfield id={userfield_id} has no LIST attribute."
        )

    enum_map: Dict[str, str] = {}

    for item in enum_list:
        item_id = item.get("ID")
        value = item.get("VALUE")

        if item_id and value:
            enum_map[item_id] = value

    if not enum_map:
        raise RuntimeError(
            f"Enum map is empty for userfield id={userfield_id}"
        )

    return enum_map
