import logging

import requests
from requests.exceptions import RequestException

from src.config import ZAPI_CLIENT_TOKEN, ZAPI_INSTANCE_ID, ZAPI_TOKEN

logger = logging.getLogger(__name__)


def is_instance_connected(timeout: int = 5) -> bool:
    url = f'https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/status'
    headers = {'Client-Token': ZAPI_CLIENT_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if not response.ok:
            logger.warning(
                'Z-API respondeu com status %s: %s', response.status_code, response.text
            )

        data = response.json()
        connected = data.get('connected', False)

        if not connected:
            logger.warning(
                'Z-API reportou instância desconectada: %s',
                data.get('error', 'sem detalhes'),
            )

        return bool(connected)
    except RequestException as error:
        logger.error('Falha ao verificar status da instância Z-API: %s', error)
        return False
    except ValueError:
        logger.error('Falha ao interpretar resposta JSON da Z-API ao verificar status')
        return False


def send_message(phone: str, name: str) -> bool:
    url = f'https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text'

    formatted_name = name.title()

    payload = {
        'phone': phone,
        'message': f'Olá, {formatted_name} tudo bem com você?',
    }

    headers = {'Client-Token': ZAPI_CLIENT_TOKEN}

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    body = response.json()

    if isinstance(body, dict):
        if body.get('error') or body.get('errors'):
            logger.error(f'Resposta de erro da Z-API ao enviar para {name}: {body}')
            return False

    return True
