"""
XLSX export integration test.

Validates:
- Deal normalization
- XLSX file generation

Run this test with:
    $ python -m tests.test_xlsx_export
"""

from src.normalizers.deal_export_normalizer import normalize_deal_for_export
from src.exporters.xlsx_exporter import export_deals_to_xlsx


def run() -> None:
    print("Starting XLSX export test...\n")

    # Minimal mock enriched deal
    enriched_deals = [
        {
            "pipeline": "Pré vendas",
            "stage": "Contato inicial",
            "company": "ACME LTDA",
            "responsible": "João Silva",
            "deal_name": "Venda Teste",
            "type": "SALE",
            "source": "Formulário de CRM",
            "revenue": 1000.0,
            "created_at": "01/01/2025",
            "start_date": "01/01/2025",
            "close_date": "10/01/2025",
            "order_description": None,
            "consultant_name": None,
            "management": "Inside Sales",
            "advanced_sale_type": "Vivo Voz Negócios",
            "devices_total_value": None,
            "document_type": "CNPJ",
        }
    ]

    normalized = [normalize_deal_for_export(d) for d in enriched_deals]

    export_deals_to_xlsx(
        deals=normalized,
        output_path="deals_export_test.xlsx",
    )

    print("XLSX export test completed successfully.")
    print("File generated: deals_export_test.xlsx")


if __name__ == "__main__":
    run()
