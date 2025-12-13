"""
Deal export normalizer.

Responsible for:
- Translating internal field names to final spreadsheet labels
- Applying final formatting rules
- Producing export-ready dictionaries
"""

from typing import Dict, Any


FIELD_LABEL_MAP: Dict[str, str] = {
    "pipeline": "Pipeline",
    "stage": "Fase",
    "company": "Empresa",
    "responsible": "Responsável",
    "deal_name": "Nome do Negócio",
    "type": "Tipo",
    "source": "Fonte",
    "revenue": "Renda",
    "created_at": "Criado em",
    "start_date": "Data de Início",
    "close_date": "Data de Fechamento",
    "order_description": "Descrição do Pedido",
    "consultant_name": "Nome do Consultor",
    "management": "Gerência",
    "advanced_sale_type": "Tipo de Venda Avançados",
    "devices_total_value": "Valor Total de Aparelhos",
    "document_type": "Tipo de Documento",
}


def normalize_deal_for_export(deal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts an enriched deal into an export-ready structure.
    """

    normalized: Dict[str, Any] = {}

    for internal_key, value in deal.items():
        label = FIELD_LABEL_MAP.get(internal_key, internal_key)

        # Final presentation rules
        if value is None:
            normalized[label] = ""
        else:
            normalized[label] = value

    return normalized
