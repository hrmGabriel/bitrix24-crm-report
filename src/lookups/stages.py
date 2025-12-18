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

    pipeline_ids = list(pipeline_map.keys())
    total = len(pipeline_ids)

    print(f"Resolving stages... 0/{total}", end="", flush=True)

    for index, category_id in enumerate(pipeline_ids, start=1):
        # This endpoint is NOT paginated according to Bitrix API docs
        response = client.call(
            "crm.dealcategory.stage.list",
            {"id": category_id},
        )

        stages = response.get("result", [])

        if not stages:
            print(f"\rResolving stages... {index}/{total}", end="", flush=True)
            continue

        stage_map[category_id] = {}

        for stage in stages:
            try:
                status_id = stage["STATUS_ID"]
                stage_name = stage["NAME"]
            except KeyError:
                continue

            stage_map[category_id][status_id] = stage_name

        # Dynamic progress update
        print(f"\rResolving stages... {index}/{total}", end="", flush=True)

    print()

    if not stage_map:
        raise RuntimeError(
            "No deal stages found. "
            "Please verify permissions for crm.dealcategory.stage.list."
        )

    return stage_map
