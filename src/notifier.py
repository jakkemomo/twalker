from abc import abstractmethod

import telegram

from src.utils import SingletonMeta, logger, get_environment_variable


class Notifier(metaclass=SingletonMeta):
    @abstractmethod
    def notify(self, *args, **kwargs) -> None:
        pass


class TelegramNotifier(Notifier):
    def __init__(self):
        self._chat_id = get_environment_variable('TELEGRAM_CHAT_ID')
        self._token = get_environment_variable('TELEGRAM_BOT_TOKEN')
        self._bot = telegram.Bot(token=self._token)

    def notify(self, data) -> None:
        logger.info(f"New notification: {data}")
        self._bot.send_message(text='https://twitter.com/elonmusk/status/1486846468887560201', chat_id=self._chat_id)
