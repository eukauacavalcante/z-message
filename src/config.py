import os

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
ZAPI_INSTANCE_ID = os.getenv('ZAPI_INSTANCE_ID')
ZAPI_TOKEN = os.getenv('ZAPI_TOKEN')
ZAPI_CLIENT_TOKEN = os.getenv('ZAPI_CLIENT_TOKEN')

required = {
    'SUPABASE_URL': SUPABASE_URL,
    'SUPABASE_SERVICE_ROLE_KEY': SUPABASE_SERVICE_ROLE_KEY,
    'ZAPI_INSTANCE_ID': ZAPI_INSTANCE_ID,
    'ZAPI_TOKEN': ZAPI_TOKEN,
    'ZAPI_CLIENT_TOKEN': ZAPI_CLIENT_TOKEN,
}

missing = [key for key, value in required.items() if not value]
if missing:
    raise EnvironmentError(f'Variáveis de ambiente faltando: {", ".join(missing)}')
