import datetime
import logging
import os
from abc import abstractmethod

import requests

from src.utils import SingletonMeta


class InformationSource(metaclass=SingletonMeta):
    _urls = set()

    def add_url(self, url):
        self._urls.add(url)

    def parse(self) -> dict:
        data = {}
        for url in self._urls:
            response = self._request_information(url)
            if response:
                data[url] = response
        return data

    @abstractmethod
    def _request_information(self, url, *args, **kwargs) -> dict:
        pass


class TwitterSource(InformationSource):

    def __init__(self, max_results=15):
        self.type = 'twitter'
        self.max_results = max_results
        self._headers = {"Authorization": f"Bearer {self._token}"}

        time_now = datetime.datetime.now()
        self._end_time = (time_now + datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        self._start_time = (time_now - datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _request_information(self, user_id, *args, **kwargs):
        url = self._create_url(user_id, self._start_time, self._end_time, self.max_results)
        json_response = {}
        try:
            json_response = self._connect_to_endpoint(url[0], self._headers, url[1])
        except ConnectionError as e:
            logging.error(e)
        return json_response

    @staticmethod
    def _create_url(user_id, start_date, end_date, max_results=10):
        search_url = "https://api.twitter.com/2/tweets/search/all"  # Change to the endpoint you want to collect data from

        # change params based on the endpoint you are using
        query_params = {'query': user_id,
                        'start_time': start_date,
                        'end_time': end_date,
                        'max_results': max_results,
                        'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                        'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                        'next_token': {}}
        return search_url, query_params

    @staticmethod
    def _connect_to_endpoint(url, headers, params, next_token=None):
        params['next_token'] = next_token  # params object received from create_url function
        response = requests.request("GET", url, headers=headers, params=params)
        print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise ConnectionError(response.status_code, response.text)
        return response.json()

    @property
    def _token(self):
        token = os.getenv('TWITTER_TOKEN')
        if not token:
            raise ValueError(
                """Twitter token is not set.
                 Please set environment variable called TWITTER_TOKEN with value of your twitter access key."""
            )
        return token
