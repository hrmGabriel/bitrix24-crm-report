"""
Deal enrichment utilities.

Responsible for:
- Translating IDs to human-readable values
- Normalizing date formats
- Preparing final deal records for reporting
"""

from typing import Dict, List
from datetime import datetime, timedelta, timezone

def normalize_datetime(date_str: str | None) -> str | None:
    """
    Converts Bitrix datetime (UTC+3) to UTC-3 and formats as dd/mm/yyyy.
    """

    if not date_str:
        return None

    try:
        dt = datetime.fromisoformat(date_str)
        dt = dt.astimezone(timezone(timedelta(hours=-3)))
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return None

def extract_stage_status_id(stage_id: str | None) -> str | None:
    """
    Extracts STATUS_ID from STAGE_ID (e.g. C8:WON -> WON)
    """

    if not stage_id or ":" not in stage_id:
        return None

    return stage_id.split(":", 1)[1]

def enrich_deals(
    deals: List[Dict],
    pipeline_map: Dict[int, str],
    stage_map: Dict[int, Dict[str, str]],
    company_map: Dict[int, str],
    user_map: Dict[int, str],
    source_status_map: Dict[str, str],
    management_enum_map: Dict[str, str],
) -> List[Dict]:
    """
    Enriches raw deal data into report-ready records.
    """

    enriched: List[Dict] = []

    for deal in deals:
        category_id = int(deal.get("CATEGORY_ID", 0))
        stage_status_id = extract_stage_status_id(deal.get("STAGE_ID"))

        enriched.append({
            "pipeline": pipeline_map.get(category_id),
            "stage": stage_map.get(category_id, {}).get(stage_status_id),
            "company": company_map.get(int(deal["COMPANY_ID"])) if deal.get("COMPANY_ID") else None,
            "responsible": user_map.get(int(deal["ASSIGNED_BY_ID"])) if deal.get("ASSIGNED_BY_ID") else None,
            "deal_name": deal.get("TITLE"),
            "type": deal.get("TYPE_ID"),
            "source": source_status_map.get(deal.get("SOURCE_ID")),
            "revenue": deal.get("OPPORTUNITY"),
            "created_at": normalize_datetime(deal.get("DATE_CREATE")),
            "start_date": normalize_datetime(deal.get("BEGINDATE")),
            "close_date": normalize_datetime(deal.get("CLOSEDATE")),
            "order_description": deal.get("UF_CRM_1750948742478"),
            "consultant_name": deal.get("UF_CRM_1750950619818"),
            "management": management_enum_map.get(deal.get("UF_CRM_1750951091402")),
            "advanced_sale_type": deal.get("UF_CRM_1751306725382"),
            "devices_total_value": deal.get("UF_CRM_1751332724412"),
            "document_type": deal.get("UF_CRM_1753968931293"),
        })

    return enriched
