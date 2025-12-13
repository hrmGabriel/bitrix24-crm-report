"""
Deal enrichment integration test.

Validates:
- End-to-end enrichment of CRM deals
- Proper lookup resolution (users, companies, stages, enums)
- Output structure ready for reporting

Run this test with:
    $ python -m tests.deal_enrichment
"""

from src.bitrix_client import BitrixClient
from src.config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK

from src.loaders.deals import fetch_deals
from src.lookups.pipelines import fetch_pipeline_map
from src.lookups.stages import fetch_stage_map
from src.lookups.users import fetch_user_map
from src.lookups.companies import fetch_company_map
from src.lookups.statuses import fetch_status_map
from src.lookups.userfield_enums import fetch_userfield_enum_map

from src.enrichers.deals import enrich_deals


# Internal ID of the "Gerência" userfield enum
GERENCIA_USERFIELD_ID = 261


def run() -> None:
    print("Starting deal enrichment integration test...\n")

    client = BitrixClient(
        base_url=BITRIX_URL,
        user_id=BITRIX_USER_ID,
        webhook=BITRIX_WEBHOOK,
    )

    # Load raw data
    deals = fetch_deals(
        client=client,
        start_date="2025-12-12"
    )
    print(f"Deals loaded: {len(deals)}")

    company_ids = {
        int(deal["COMPANY_ID"])
        for deal in deals
        if deal.get("COMPANY_ID")
    }


    pipeline_map = fetch_pipeline_map(client)
    stage_map = fetch_stage_map(client, pipeline_map)
    user_map = fetch_user_map(client)
    company_map = fetch_company_map(client=client, company_ids=company_ids)
    source_status_map = fetch_status_map(client, entity_id="SOURCE")
    gerencia_enum_map = fetch_userfield_enum_map(
        client=client,
        userfield_id=GERENCIA_USERFIELD_ID
    )

    # Enrich
    enriched_deals = enrich_deals(
        deals=deals,
        pipeline_map=pipeline_map,
        stage_map=stage_map,
        company_map=company_map,
        user_map=user_map,
        source_status_map=source_status_map,
        management_enum_map=gerencia_enum_map,
    )

    print(f"Enriched deals: {len(enriched_deals)}\n")

    # Basic assertions (manual-style, non-fatal)
    if not enriched_deals:
        raise RuntimeError("No enriched deals produced")

    sample = enriched_deals[0]

    required_fields = [
        "pipeline",
        "stage",
        "deal_name",
        "responsible",
        "company",
        "created_at",
    ]

    for field in required_fields:
        if field not in sample:
            raise RuntimeError(f"Missing expected field: {field}")

    print("Sample enriched deal:\n")
    for key, value in sample.items():
        print(f"{key}: {value}")

    print("\nDeal enrichment test completed successfully.")


if __name__ == "__main__":
    run()
