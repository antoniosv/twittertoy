import unittest
from unittest import mock
from twitter_api import TwitterApi

import config.config as config

import requests


class TwitterApiTest(unittest.TestCase):

    def setUp(self):
        self.app = config.App()

    def test_convertTwitterDate(self):
        twitter_api = TwitterApi()
        date_twitter = 'Sun Sep 27 15:50:28 +0000 2020'

        actual = twitter_api.convertTwitterDate(date_twitter)

        expected = '15:50 PM - 27 Sep 2020'

        self.assertEqual(expected, actual)

    def test_createAuthHeader(self):
        twitter_api = TwitterApi()

        actual = twitter_api.createAuthHeader()

        expected = {"Authorization": "Bearer bearer_token"}

        self.assertEqual(expected, actual)

    def test_extractHashtags(self):
        twitter_api = TwitterApi()

        hashtags = [
            {'text': 'three'},
            {'text': 'seagrass'}
        ]

        actual = twitter_api.extractHashtags(hashtags)

        expected = ['three', 'seagrass']

        self.assertEqual(expected, actual)

    def test_createSearchUrlHashtag(self):
        twitter_api = TwitterApi()

        actual = twitter_api.createSearchUrlHashtag('%%23influencer', '5')

        expected = 'https://api.twitter.com/1.1/search/tweets.json?q=%%23influencer&count=5'

        self.assertEqual(expected, actual)

    @mock.patch("requests.get")
    @mock.patch("twitter_api.TwitterApi.createSearchUrlHashtag")
    @mock.patch("twitter_api.TwitterApi.createAuthHeader")
    def test_getTweetsByHashtag_obtainResultFromApiSuccessfully(self, mocked_header, mocked_url, mocked_get):
        twitter_api = TwitterApi()

        mocked_url.return_value = "api_url"
        mocked_header.return_value = "header"

        json_response = "json_response"
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = json_response

        twitter_api.getTweetsByHashtag('hashtag', '3')

        mocked_get.assert_called_with("api_url", headers="header")

    @mock.patch("requests.get")
    @mock.patch("twitter_api.TwitterApi.createSearchUrlHashtag")
    @mock.patch("twitter_api.TwitterApi.createAuthHeader")
    def test_getTweetsByHashtag_handleExceptionOnApiBadRequest(self, mocked_header, mocked_url, mocked_get):
        twitter_api = TwitterApi()

        mocked_url.return_value = "api_url"
        mocked_header.return_value = "header"

        json_response = "json_response"
        mocked_get.return_value.status_code = 400
        mocked_get.return_value.text = json_response

        with self.assertRaises(Exception):
            twitter_api.getTweetsByHashtag('hashtag', '3')

        mocked_get.assert_called_with("api_url", headers="header")
