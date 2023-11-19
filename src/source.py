import copy
import datetime
from abc import abstractmethod

import pytz
import requests

from src.settings import DEFAULT_SLEEP_TIME, FOLLOWER_COUNT_LIMIT
from src.utils import SingletonMeta, logger, get_environment_variable


class InformationSource(metaclass=SingletonMeta):
    _urls = set()

    def add_url(self, url) -> None:
        self._urls.add(url)

    def parse(self) -> dict:
        data = {}
        for url in self._urls:
            response = self._request_information(url)
            if response:
                data[url] = response
        return data

    @abstractmethod
    def _request_information(self, url) -> dict:
        ...


class TwitterSource(InformationSource):

    def __init__(self, max_results=25):
        self.type = 'twitter'
        self.max_results = max_results
        self._token = get_environment_variable('TWITTER_TOKEN')
        self._headers = {"Authorization": f"Bearer {self._token}"}

        time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self._start_time = (time_now - datetime.timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _request_information(self, user_id) -> dict:
        messages = {}
        try:
            influences_messages = self._get_influencer_messages(user_id)
            related_messages = self._get_related_messages(user_id)
            messages = {**related_messages, **influences_messages}
            if messages:
                time_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                self._start_time = (time_now - datetime.timedelta(seconds=DEFAULT_SLEEP_TIME)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        except ConnectionError as e:
            logger.error(e)
        return messages

    @staticmethod
    def _create_influencer_url(user_id, start_date, max_results):
        search_url = "https://api.twitter.com/2/tweets/search/recent"
        query_params = {
            'query': f'from:{user_id}',
            'max_results': max_results,
            'start_time': start_date,
            'expansions': 'author_id',
            'tweet.fields': 'id,text,author_id,created_at',
            'user.fields': 'public_metrics',
        }
        return search_url, query_params

    @staticmethod
    def _create_related_url(user_id, start_date, max_results):
        search_url = "https://api.twitter.com/2/tweets/search/recent"
        query_params = {
            'query': f'to:{user_id} -is:retweet is:verified',
            'max_results': max_results,
            'start_time': start_date,
            'expansions': 'author_id',
            'tweet.fields': 'id,text,author_id,created_at',
            'user.fields': 'public_metrics',
        }
        return search_url, query_params

    @staticmethod
    def _connect_to_endpoint(url, headers, params) -> dict:
        response = requests.request("GET", url, headers=headers, params=params)
        logger.debug("Endpoint Response Code: %s", str(response.status_code))
        if response.status_code != 200:
            raise ConnectionError(response.status_code, response.text)
        return response.json()

    def _get_influencer_messages(self, user_id):
        influencer_url = self._create_influencer_url(user_id, self._start_time, self.max_results)
        json_response = self._connect_to_endpoint(influencer_url[0], self._headers, influencer_url[1])
        messages = {}
        if len(json_response) > 1:
            user = json_response.get('includes').get('users')[0]
            for tweet in json_response.get('data'):
                text = tweet['text']
                created_at = tweet['created_at']
                username = user['name']
                if messages.get(username):
                    messages[username] = f"{messages[username]} \n {created_at} \n {text}"
                else:
                    messages[username] = f"{created_at} \n {text}"
        return messages

    def _get_related_messages(self, user_id):
        related_url = self._create_related_url(user_id, self._start_time, self.max_results)
        json_response = self._connect_to_endpoint(related_url[0], self._headers, related_url[1])
        messages = {}
        if len(json_response) > 1:
            tweets: list = json_response.get('data')
            users: list = json_response.get('includes').get('users')

            tweets_copy: list = copy.copy(tweets)
            users_copy: list = copy.copy(users)

            for tweet_info in zip(tweets_copy, users_copy):
                tweet = tweet_info[0]
                user = tweet_info[1]
                followers_count = user['public_metrics']['followers_count']
                if followers_count < FOLLOWER_COUNT_LIMIT:
                    index = tweets.index(tweet)
                    tweets.pop(index)
                    index = users.index(user)
                    users.pop(index)
                    continue
                text = tweet['text']
                created_at = tweet['created_at']
                username = user['name']
                if messages.get(username):
                    messages[username] = f"{messages[username]} \n {created_at} \n {text}"
                else:
                    messages[username] = f"{created_at} \n {text}"
        return messages
