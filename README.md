# **Bitrix24 CRM Report**

Este repositório contém uma aplicação em Python que **extrai dados do CRM Bitrix24 via API**, enriquece esses dados com informações auxiliares (lookups) e exporta o resultado final para uma **planilha do Google Sheets**.  
O objetivo principal é **automatizar relatórios e dashboards** baseados nos dados de *Deals* (Negócios) do CRM.

---

## **O que este projeto faz**

Em alto nível, a aplicação executa os seguintes passos:

1. **Conecta-se à API REST do Bitrix24**  
   Utiliza credenciais de webhook para acessar o CRM de forma segura.

2. **Carrega os negócios (Deals)**  
   Busca os negócios criados a partir de uma data definida (normalmente a partir do dia anterior ou de uma data inicial específica).

3. **Monta mapas de lookup**  
   Resolve IDs retornados pela API para valores legíveis, como:
   - Pipelines
   - Fases dos negócios
   - Usuários responsáveis
   - Empresas
   - Status (ex.: origem do negócio)
   - Campos enumerados (ex.: gerência, tipo de documento)

4. **Enriquece os negócios**  
   Combina os dados brutos dos negócios com os valores resolvidos nos lookups.

5. **Normaliza os dados para exportação**  
   Formata datas, traduz códigos internos (ex.: `"SALE"` → `"Vendas"`) e organiza os campos em um formato consistente.

6. **Exporta para o Google Sheets**  
   Grava os dados finais em uma planilha do Google Sheets, pronta para uso em relatórios e dashboards.

---

## **Para quem este projeto foi feito**

Este projeto é indicado para:

- Analistas de vendas
- Administradores de CRM
- Pessoas responsáveis por relatórios e BI
- Qualquer pessoa que precise automatizar a extração de dados do Bitrix24 para planilhas

Não é necessário conhecimento avançado em programação para **executar** o projeto, apenas configuração básica.

---

## **Estrutura do projeto**

```bash
├── .env.example # Exemplo de variáveis de ambiente
├── README.md # Este arquivo
├── requirements.txt # Dependências do Python
├── src/ # Código principal da aplicação
│ ├── bitrix_client.py # Cliente da API do Bitrix24
│ ├── config.py # Configurações e variáveis de ambiente
│ ├── loaders/ # Carregamento de dados brutos do CRM
│ ├── lookups/ # Construção dos mapas de lookup
│ ├── enrichers/ # Enriquecimento dos dados
│ ├── normalizers/ # Normalização para exportação
│ └── exporters/ # Exportadores (Google Sheets)
└── tests/ # Testes de integração
```

---

## **Pré-requisitos**

Antes de executar a aplicação, você precisará de:

### **1. Credenciais do Bitrix24**

Criar um webhook no Bitrix24 e obter:

- `BITRIX_URL`
- `BITRIX_USER_ID`
- `BITRIX_WEBHOOK`

Essas informações devem ser colocadas no arquivo `.env`.

---

### **2. Credenciais do Google Sheets**

1. Ativar a **Google Sheets API** no Google Cloud.
2. Criar uma **Service Account**.
3. Baixar o arquivo JSON de credenciais e salvá-lo como: `credentials.json`

4. Compartilhar a planilha do Google Sheets com o e-mail da Service Account.
5. Informar o ID da planilha no `.env`: `GOOGLE_SHEET_ID=<id-da-planilha>`


---

## **Instalação**

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais.

## **Execução do pipeline**

Para executar o pipeline completo de exportação:

```bash
python -m src.main
```

Por padrão, a aplicação:

Busca negócios a partir da data configurada

Atualiza a aba `"Folha1"` da planilha do Google Sheets

### **Como o fluxo funciona (visão geral)**

| Etapa                      | Descrição                                           |
| -------------------------- | --------------------------------------------------- |
| **Carregamento dos Deals** | Busca os negócios no Bitrix24 com filtro de data.   |
| **Lookups**                | Converte IDs retornados pela API em nomes legíveis. |
| **Enriquecimento**         | Combina dados brutos com os lookups.                |
| **Normalização**           | Ajusta formatos, traduções e rótulos.               |
| **Exportação**             | Envia os dados finais para o Google Sheets.         |

---

## **Testes**

O projeto inclui testes de integração localizados na pasta tests/, que validam:
- Conexão com a API do Bitrix24.
- Construção dos lookups.
- Execução do pipeline completo.
- Exportação para o Google Sheets.

Exemplo de execução:

```bash
python -m tests.test_full_export_pipeline
```