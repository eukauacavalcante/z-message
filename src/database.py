import logging
import re

from supabase import create_client

from src.config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL

logger = logging.getLogger(__name__)


def is_valid_phone(phone: str) -> bool:
    return bool(re.fullmatch(r'55\d{10,11}', phone))


def get_contacts(limit: int = 3) -> list[dict]:
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        response = client.table('contacts').select('name, phone').limit(limit).execute()
    except Exception as e:
        raise RuntimeError(f'Erro ao buscar contatos no banco de dados: {e}')

    valid_contacts = []

    for contact in response.data:
        if not contact.get('name', '').strip():
            logger.warning(
                f'Contato ignorado: nome ausente para telefone final {contact["phone"][-4:]}'
            )
            continue

        if not is_valid_phone(contact['phone']):
            logger.warning(
                f'Contato ignorado: telefone inválido para contato {contact["name"]}'
            )
            continue

        valid_contacts.append(contact)

    return valid_contacts
