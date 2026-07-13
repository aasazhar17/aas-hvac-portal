import os
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

ADMIN_PASSKEY = os.getenv("ADMIN_PASSKEY", "AAS_ADMIN_ARSHAD_2026")
SALES_PASSKEY = os.getenv("SALES_PASSKEY", "AAS_SALES_CRM_2026")
EDITOR_PASSKEY = os.getenv("EDITOR_PASSKEY", "AAS_EDITOR_CONTENT_2026")
SECRET_KEY = os.getenv("SECRET_KEY", "default-fallback-secret-key-12345")
