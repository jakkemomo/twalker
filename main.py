import time
from typing import List

from src.notifier import Notifier, TelegramNotifier
from src.settings import DEFAULT_SLEEP_TIME
from src.source import InformationSource, TwitterSource


def main(notifiers: List[Notifier], information_sources: List[InformationSource]) -> None:
    while True:
        for source in information_sources:
            messages: dict = source.parse()
            if messages:
                for notifier in notifiers:
                    notifier.notify(messages)
        time.sleep(DEFAULT_SLEEP_TIME)


def start():
    print('Program is going to use Twitter as a main source and Telegram as a notifier')
    telegram_notifier = TelegramNotifier()
    twitter = TwitterSource()
    running = True
    account_name = input('Add name of the twitter account (e.g. elonmusk):\n')
    twitter.add_url(account_name)
    while running:
        user_input = input('Enter Finish to start the program or enter another account name:\n')
        if user_input != 'Finish':
            twitter.add_url(user_input)
        else:
            running = False
    client_sources = [twitter]
    client_notifiers = [telegram_notifier]
    main(client_notifiers, client_sources)


if __name__ == '__main__':
    start()
