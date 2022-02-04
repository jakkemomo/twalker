import time
from typing import List

from src.notifier import Notifier, TelegramNotifier
from src.source import InformationSource, TwitterSource


def main(notifiers: List[Notifier], information_sources: List[InformationSource]) -> None:
    while True:
        for source in information_sources:
            messages: dict = source.parse()
            if messages:
                for notifier in notifiers:
                    notifier.notify(messages)
        time.sleep(10)


if __name__ == '__main__':
    telegram_notifier = TelegramNotifier()
    twitter = TwitterSource()
    twitter.add_url('1234')
    twitter.add_url('12345')
    client_sources = [twitter]
    client_notifiers = [telegram_notifier]
    main(client_notifiers, client_sources)
