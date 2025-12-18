"""
Google Sheets export integration test.

Validates:
- Authentication with Google Sheets API
- Data upload
- Column auto-resize

Run this test with:
    $ python -m tests.test_google_sheets_export
"""

from src.exporters.google_sheets_exporter import export_to_google_sheets
from src.config import GOOGLE_SHEET_ID


def run() -> None:
    print("Starting Google Sheets export test...\n")

    headers = [
        "Pipeline",
        "Fase",
        "Empresa",
        "Responsável",
        "Nome do Negócio",
        "Tipo",
        "Fonte",
        "Renda",
        "Criado em",
        "Data de Início",
        "Data de Fechamento",
        "Descrição do Pedido",
        "Nome do Consultor",
        "Gerência",
        "Tipo de Venda Avançados",
        "Valor Total de Aparelhos",
        "Tipo de Documento",
    ]

    rows = [
        {
            "Pipeline": "Pré vendas",
            "Fase": "Contato inicial",
            "Empresa": "ACME LTDA",
            "Responsável": "João Silva",
            "Nome do Negócio": "Negócio",
            "Tipo": "Vendas",
            "Fonte": "CRM",
            "Renda": "1500.00",
            "Criado em": "11/12/2025",
            "Data de Início": "13/12/2025",
            "Data de Fechamento": "13/12/2025",
            "Descrição do Pedido": "Descrição",
            "Nome do Consultor": "Consultor",
            "Gerência": "Gerente 1",
            "Tipo de Venda Avançados": "Venda avançado",
            "Valor Total de Aparelhos": "1000.00",
            "Tipo de Documento": "CPF",
        },
        {
            "Pipeline": "Inside Sales",
            "Fase": "Fase",
            "Empresa": "Empresa LTDA",
            "Responsável": "João Silva",
            "Nome do Negócio": "Negócio",
            "Tipo": "Vendas",
            "Fonte": "",
            "Renda": "200.00",
            "Criado em": "10/11/2025",
            "Data de Início": "15/11/2025",
            "Data de Fechamento": "15/11/2025",
            "Descrição do Pedido": "",
            "Nome do Consultor": "Consultor",
            "Gerência": "Gerente 2",
            "Tipo de Venda Avançados": "Venda",
            "Valor Total de Aparelhos": "500.00",
            "Tipo de Documento": "CNPJ",
        },
    ]

    export_to_google_sheets(
        spreadsheet_id=GOOGLE_SHEET_ID,
        sheet_name="Folha1",
        rows=rows,
        credentials_path="credentials.json",
        headers=headers,
    )

    print("Google Sheets export test completed successfully.")


if __name__ == "__main__":
    run()
