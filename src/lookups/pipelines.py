"""
Pipeline (Deal Category) lookup utilities.

Responsible for:
- Fetching all deal categories (pipelines)
- Building an ID → Name mapping
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_pipeline_map(client: BitrixClient) -> Dict[int, str]:
    """
    Fetches all deal pipelines and returns a mapping:
    { category_id: category_name }

    Example:
    {
        1: "Sales",
        15: "Inside Sales"
    }
    """
    
    # This endpoint is paginated according to Bitrix API docs, which is handled by call_all
    categories = client.call_all("crm.dealcategory.list")

    pipeline_map: Dict[int, str] = {}

    for category in categories:
        try:
            category_id = int(category["ID"])
            category_name = category["NAME"]
        except KeyError:
            # Ignore malformed entries
            continue

        pipeline_map[category_id] = category_name

    if not pipeline_map:
        raise RuntimeError(
            "No deal categories found. "
            "Please verify API permissions for crm.dealcategory.list."
        )

    return pipeline_map
