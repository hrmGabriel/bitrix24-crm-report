"""
Deal export pipeline.

Responsible for:
- Loading deals from Bitrix
- Enriching deals with lookup data
- Normalizing deals for export
- Writing the final XLSX file
"""

from datetime import datetime, timedelta
from typing import List

from src.loaders import deals
from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK, GOOGLE_SHEET_ID

from src.loaders.deals import fetch_deals
from src.enrichers.deals import enrich_deals

from src.normalizers.deal_export_normalizer import normalize_deal_for_export
from src.exporters.xlsx_exporter import export_deals_to_xlsx
from src.exporters.google_sheets_exporter import export_to_google_sheets

from src.lookups.pipelines import fetch_pipeline_map
from src.lookups.stages import fetch_stage_map
from src.lookups.users import fetch_user_map
from src.lookups.companies import fetch_company_map
from src.lookups.statuses import fetch_status_map
from src.lookups.userfield_enums import fetch_userfield_enum_map


def run_export(days_back: int = 1) -> None:
    """
    Runs the full deal export pipeline.

    Args:
        days_back: How many days back to fetch deals from
    """

    print("Starting deal export pipeline...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK,
    )

    start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    # 1. Load deals
    print("Loading deals...")
    deals = fetch_deals(
        client=client,
        start_date=start_date,
    )
    print(f"Deals loaded: {len(deals)}\n")

    if not deals:
        print("No deals found. Aborting export.")
        return

    # 2. Build lookup maps
    print("Building lookup maps...")

    pipeline_map = fetch_pipeline_map(client)
    stage_map = fetch_stage_map(client, pipeline_map)
    user_map = fetch_user_map(client)

    company_ids = {deal.get("COMPANY_ID") for deal in deals if deal.get("COMPANY_ID")}
    company_map = fetch_company_map(client, company_ids)

    SOURCE_ENTITY_ID = "SOURCE"

    source_status_map = fetch_status_map(
        client=client,
        entity_id=SOURCE_ENTITY_ID,
    )

    GERENCIA_USERFIELD_ID = 261
    gerencia_enum_map = fetch_userfield_enum_map(
        client=client,
        userfield_id=GERENCIA_USERFIELD_ID,
    )

    print("Lookup maps ready.\n")

    # 3. Enrich deals
    print("Enriching deals...")

    enriched_deals = enrich_deals(
        deals=deals,
        pipeline_map=pipeline_map,
        stage_map=stage_map,
        company_map=company_map,
        user_map=user_map,
        source_status_map=source_status_map,
        management_enum_map=gerencia_enum_map,
    )

    print(f"Deals enriched: {len(enriched_deals)}\n")

    # 4. Normalize for export
    print("Normalizing deals...")
    normalized_deals = [
        normalize_deal_for_export(deal)
        for deal in enriched_deals
    ]

    # 5. Export to XLSX
    """
    output_file = "bitrix_deals_export.xlsx"
    print(f"Exporting to XLSX: {output_file}")

    export_deals_to_xlsx(
        deals=normalized_deals,
        output_path=output_file,
    )
    """

    # 6. Export to Google Sheets
    export_to_google_sheets(
        spreadsheet_id=GOOGLE_SHEET_ID,
        sheet_name="Folha1",
        rows=normalized_deals,
        credentials_path="credentials.json",
    )

    print("\nDeal export pipeline completed successfully.")
