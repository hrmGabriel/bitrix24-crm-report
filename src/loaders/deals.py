"""
Deal loader utilities.

Responsible for:
- Fetching deals from Bitrix24 CRM
- Handling pagination safely
- Returning raw deal data for further enrichment
"""

from typing import List, Dict, Any
from src.bitrix_client import BitrixClient


DEAL_SELECT_FIELDS = [
    "ID",
    "TITLE",
    "TYPE_ID",
    "STAGE_ID",
    "CATEGORY_ID",
    "COMPANY_ID",
    "ASSIGNED_BY_ID",
    "SOURCE_ID",
    "OPPORTUNITY",
    "DATE_CREATE",
    "BEGINDATE",
    "CLOSEDATE",

    # Custom fields
    "UF_CRM_1750948742478",  # Descrição do Pedido
    "UF_CRM_1750950619818",  # Nome do Consultor
    "UF_CRM_1750951091402",  # Gerência
    "UF_CRM_1751306725382",  # Tipo de Venda Avançados
    "UF_CRM_1751332724412",  # Valor Total de Aparelhos
    "UF_CRM_1753968931293",  # Tipo de Documento
]



def fetch_deals(
    client: BitrixClient,
    start_date: str | None = None,
    progress_callback=None,
) -> List[Dict[str, Any]]:
    """
    Fetches CRM deals with optional date filtering.

    Args:
        start_date: ISO date string (YYYY-MM-DD).
                    If provided, only deals created on or after this date are fetched.
        progress_callback: Optional callback to report loading progress.
    """

    payload: Dict[str, Any] = {
        "select": DEAL_SELECT_FIELDS
    }

    if start_date:
        payload["filter"] = {
            ">=DATE_CREATE": start_date
        }

    # Delegate progress reporting to Bitrix client pagination
    return client.call_all(
        "crm.deal.list",
        payload,
        progress_callback=progress_callback,
    )

