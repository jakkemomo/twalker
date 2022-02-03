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
        self._token = self.get_telegram_token()
        self._bot = telegram.Bot(token=self._token)

    @staticmethod
    def get_telegram_token():
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError(
                """Telegram token is not set.
                 Please set environment variable called TELEGRAM_BOT_TOKEN with value of your telegram token."""
            )
        return token

    def notify(self, data):
        logger.info(f"Notification from Twitter: {data}")
        self._bot.send_message(text='https://twitter.com/elonmusk/status/1486846468887560201', chat_id=-746170969)


if __name__ == "__main__":
    notifier1 = TelegramNotifier()
    notifier2 = TelegramNotifier()
    notifier3 = TelegramNotifier()
    notifier4 = TelegramNotifier()
    if id(notifier1) == id(notifier2) == id(notifier3) == id(notifier4):
        print("Success")
