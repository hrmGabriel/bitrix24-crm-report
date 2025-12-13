"""
Deal stage (phase) lookup utilities.

Responsible for:
- Fetching stages for each pipeline
- Building a nested lookup:
  { category_id: { status_id: stage_name } }
"""

from typing import Dict
from src.bitrix_client import BitrixClient


def fetch_stage_map(
    client: BitrixClient,
    pipeline_map: Dict[int, str],
) -> Dict[int, Dict[str, str]]:
    """
    Fetches stages for each pipeline and returns a nested mapping.

    Example:
    {
        15: {
            "LOSE": "Lost",
            "WON": "Won"
        }
    }
    """

    stage_map: Dict[int, Dict[str, str]] = {}

    for category_id in pipeline_map.keys():
        response = client.call(
            "crm.dealcategory.stage.list",
            {"id": category_id},
        )

        stages = response.get("result", [])

        if not stages:
            continue

        stage_map[category_id] = {}

        for stage in stages:
            try:
                status_id = stage["STATUS_ID"]
                stage_name = stage["NAME"]
            except KeyError:
                continue

            stage_map[category_id][status_id] = stage_name

    if not stage_map:
        raise RuntimeError(
            "No deal stages found. "
            "Please verify permissions for crm.dealcategory.stage.list."
        )

    return stage_map
