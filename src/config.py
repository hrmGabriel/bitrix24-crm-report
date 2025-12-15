import os
from dotenv import load_dotenv

load_dotenv()

BITRIX_URL = os.getenv("BITRIX_URL")
BITRIX_USER_ID = os.getenv("BITRIX_USER_ID")
BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK")

if not BITRIX_URL or not BITRIX_USER_ID or not BITRIX_WEBHOOK:
    raise RuntimeError("Configuration error: Missing required environment variables.")
