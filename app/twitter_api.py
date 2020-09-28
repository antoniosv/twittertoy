import config.config as config
import requests

from datetime import datetime


class TwitterApi():

    def __init__(self):
        app = config.App()
        self.bearer_token = app.config.get('Twitter', 'bearer_token')
        self.tweet_search_url = app.config.get('Twitter', 'tweet_search_url')
        self.user_tweets_url = app.config.get('Twitter', 'user_tweets_url')

    def createAuthHeader(self):
        """
        Create authorization header required for the Twitter API
        """
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers

    def createTweetSearchUrl(self, keyword, limit):
        """
        Setup the query parameters to the tweet search API
        """
        url = self.tweet_search_url.format(keyword) + "&count={}".format(limit)
        return url

    def createUserTweetsUrl(self, screen_name, limit):
        """
        Setup the query parameters to the user's tweet search API
        """
        url = self.user_tweets_url.format(screen_name) + "&count={}".format(limit)
        return url

    def getTweetsByHashtag(self, hashtag, limit):
        """
        Call Twitter API to get tweets by a single hashtag
        """
        auth_header = self.createAuthHeader()
        url = self.createTweetSearchUrl(hashtag, limit)
        response = requests.get(url, headers=auth_header)
        if response.status_code != requests.codes.ok:
            # TODO
            # logging
            print(url, flush=True)
            raise Exception(response.status_code, response.text)
        return response.json()

    def getTweetsByUsername(self, username, limit):
        """
        Call Twitter API to get tweets by username
        """
        auth_header = self.createAuthHeader()
        url = self.createUserTweetsUrl(username, limit)
        response = requests.get(url, headers=auth_header)
        if response.status_code != requests.codes.ok:
            # TODO
            # logging
            print(url, flush=True)
            raise Exception(response.status_code, response.text)
        return response.json()

    def extractTweetInfo(self, tweets):
        """
        Extracts the relevant info from the Twitter API response
        """
        summarized = []
        for tweet in tweets:
            summarized_tweet = {
                'account': {
                    'fullname': tweet['user']['name'],
                    'href': '/' + tweet['user']['screen_name'],
                    'id': tweet['user']['id'],
                },
                'date': self.convertTwitterDate(tweet['created_at']),
                'hashtags': self.extractHashtags(tweet['entities']['hashtags']),
                'likes': tweet['favorite_count'],
                # TODO
                # 'replies': ...,
                'retweets': tweet['retweet_count'],
                'text': tweet['text'],
            }
            summarized.append(summarized_tweet)

        return summarized

    def convertTwitterDate(self, twitter_date):
        """
        Returns twitter created_at date field to the format: 12:57 PM - 7 Mar 2018
        """
        parsed_datetime = datetime.strptime(
            twitter_date, '%a %b %d %H:%M:%S +0000 %Y')
        return parsed_datetime.strftime('%H:%M %p - %d %b %Y')

    def extractHashtags(self, hashtags):
        """
        Receives the hashtag list portion of the response, incl. metadata and
        makes a list of only the hashtag labels
        """
        merged = []
        for hashtag in hashtags:
            merged.append(hashtag['text'])
        return merged
