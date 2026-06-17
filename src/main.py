import logging

from src.database import get_contacts
from src.logger_config import setup_logging
from src.whatsapp import is_instance_connected, send_message

setup_logging()

logger = logging.getLogger(__name__)


def main():
    logger.info('Verificando conexão com a instância Z-API...')

    if not is_instance_connected():
        logger.error(
            'Instância Z-API desconectada. Verifique a conexão e tente novamente.'
        )
        return

    logger.info('Instância conectada. Buscando contatos...')

    try:
        contacts = get_contacts()
    except Exception as err:
        logger.error('Erro ao buscar contatos: %s', err)
        return

    if not contacts:
        logger.warning('Nenhum contato encontrado. Encerrando...')
        return

    logger.info(f'{len(contacts)} contato(s) encontrado(s).\n')

    for contact in contacts:
        name = contact['name']
        phone = contact['phone']
        masked_phone = phone[:4] + '****' + phone[-4:]

        logger.info(f'Enviando mensagem para {name} ({masked_phone})')
        success = send_message(phone=phone, name=name)

        if success:
            logger.info('Enviado com sucesso.')
        else:
            logger.error('Falha no envio.')


if __name__ == '__main__':
    main()
