import os
from abc import abstractmethod

import telegram

from utils import SingletonMeta, logger


class Notifier(metaclass=SingletonMeta):
    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class TelegramNotifier(Notifier):
    def __init__(self):
        self._bot = telegram.Bot(token=self._token)

    @property
    def _token(self):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError(
                """Telegram token is not set.
                 Please set environment variable called TELEGRAM_BOT_TOKEN with value of your telegram token."""
            )
        return token

    def notify(self, data):
        logger.info(f"New notification: {data}")
        self._bot.send_message(text='https://twitter.com/elonmusk/status/1486846468887560201', chat_id=-746170969)
