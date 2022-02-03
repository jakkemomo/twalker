import time
from typing import List

from notifier import Notifier, TelegramNotifier
from source import InformationSource, TwitterSource


def main(notifier: Notifier, information_sources: List[InformationSource]) -> None:
    while True:
        for source in information_sources:
            data: dict = source.parse()
            if data:
                notifier.notify(data)
        time.sleep(4)


if __name__ == '__main__':
    telegram_notifier = TelegramNotifier()
    twitter = TwitterSource()
    twitter.add_url('1234')
    twitter.add_url('12345')
    sources = [twitter]
    main(telegram_notifier, sources)
