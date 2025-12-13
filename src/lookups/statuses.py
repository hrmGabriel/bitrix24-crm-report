"""
Status lookup utilities.

Responsible for:
- Fetching CRM statuses by ENTITY_ID
- Building lookups:
  { STATUS_ID: NAME }
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_status_map(
    client: BitrixClient,
    entity_id: str
) -> Dict[str, str]:
    """
    Fetches status list for a given ENTITY_ID.

    Args:
        entity_id: e.g. "SOURCE", "DEAL_TYPE"

    Returns:
        {
            "WEBFORM": "Formulário de CRM",
            "CALL": "Chamada"
        }
    """

    statuses = client.call(
        "crm.status.list",
        payload={
            "filter": {
                "ENTITY_ID": entity_id
            }
        }
    ).get("result", [])

    if not statuses:
        raise RuntimeError(
            f"No statuses returned for ENTITY_ID={entity_id}"
        )

    status_map: Dict[str, str] = {}

    for status in statuses:
        status_id = status.get("STATUS_ID")
        name = status.get("NAME")

        if status_id and name:
            status_map[status_id] = name

    if not status_map:
        raise RuntimeError(
            f"Status map is empty for ENTITY_ID={entity_id}"
        )

    return status_map
