import logging

from telegram_eco_bot import TelegramEcoBot
from loggerinitializer import initialize_logger


def main():
    try:
        telegram_eco_bot = TelegramEcoBot()
        logging.info('Погнали!')
        telegram_eco_bot.updater.idle()
    except KeyError:
        logging.info('Добавь token, или я не буду работать!')
    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        TelegramEcoBot().send_error(error)


if __name__ == '__main__':
    initialize_logger()
    main()