import unittest
from unittest import mock
from twitter_api import TwitterApi

import config.config as config


class TwitterApiTest(unittest.TestCase):

    def setUp(self):
        app = config.App()

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

    def test_createTweetSearchUrl(self):
        twitter_api = TwitterApi()

        actual = twitter_api.createTweetSearchUrl('influencer', '5')

        expected = 'https://api.twitter.com/1.1/search/tweets.json?q=%23influencer&count=5'

        self.assertEqual(expected, actual)

    def test_createUserTweetsUrl(self):
        twitter_api = TwitterApi()

        actual = twitter_api.createUserTweetsUrl('nasa', '3')

        expected = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=nasa&count=3'

        self.assertEqual(expected, actual)

    @mock.patch("requests.get")
    @mock.patch("twitter_api.TwitterApi.createTweetSearchUrl")
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
    @mock.patch("twitter_api.TwitterApi.createTweetSearchUrl")
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

    @mock.patch("requests.get")
    @mock.patch("twitter_api.TwitterApi.createUserTweetsUrl")
    @mock.patch("twitter_api.TwitterApi.createAuthHeader")
    def test_getTweetsByUsername_obtainResultFromApiSuccessfully(self, mocked_header, mocked_url, mocked_get):
        twitter_api = TwitterApi()

        mocked_url.return_value = "api_url"
        mocked_header.return_value = "header"

        json_response = "json_response"
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.text = json_response

        twitter_api.getTweetsByUsername('hashtag', '3')

        mocked_get.assert_called_with("api_url", headers="header")

    @mock.patch("requests.get")
    @mock.patch("twitter_api.TwitterApi.createUserTweetsUrl")
    @mock.patch("twitter_api.TwitterApi.createAuthHeader")
    def test_getTweetsByUsername_handleExceptionOnApiBadRequest(self, mocked_header, mocked_url, mocked_get):
        twitter_api = TwitterApi()

        mocked_url.return_value = "api_url"
        mocked_header.return_value = "header"

        json_response = "json_response"
        mocked_get.return_value.status_code = 400
        mocked_get.return_value.text = json_response

        with self.assertRaises(Exception):
            twitter_api.getTweetsByUsername('nasa', '3')

        mocked_get.assert_called_with("api_url", headers="header")

    def test_extractTweetInfo(self):
        tweets = [
            {
                "created_at": "Thu Apr 06 15:28:43 +0000 2017",
                "text": "tweet_text_first",
                "entities": {
                    "hashtags": [{"text": "first"}, {"text": "second"}],
                },
                "user": {
                    "id": 111,
                    "name": "name_one",
                    "screen_name": "screen_name_one",
                },
                "retweet_count": 10,
                "favorite_count": 11,
            },
            {
                "created_at": "Fri Apr 16 15:28:43 +0000 2017",
                "text": "tweet_text_second",
                "entities": {
                    "hashtags": [{"text": "one"}, {"text": "two"}],
                },
                "user": {
                    "id": 222,
                    "name": "name_two",
                    "screen_name": "screen_name_two",
                },
                "retweet_count": 20,
                "favorite_count": 21,
            }
        ]

        twitter_api = TwitterApi()
        actual = twitter_api.extractTweetInfo(tweets)

        expected = [
            {
                'account': {
                    'fullname': 'name_one',
                    'href': '/screen_name_one',
                    'id': 111,
                },
                'date': '15:28 PM - 06 Apr 2017',
                'hashtags': ['first', 'second'],
                'likes': 11,
                'retweets': 10,
                'text': 'tweet_text_first',
            },
            {
                'account': {
                    'fullname': 'name_two',
                    'href': '/screen_name_two',
                    'id': 222,
                },
                'date': '15:28 PM - 16 Apr 2017',
                'hashtags': ['one', 'two'],
                'likes': 21,
                'retweets': 20,
                'text': 'tweet_text_second',
            },
        ]

        self.assertEqual(expected, actual)
