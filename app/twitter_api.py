import config.config as config
import requests

from datetime import datetime


class TwitterApi():

    tweet_fields_author = "tweet.fields=author_id"
    separator = "&"

    def __init__(self):
        app = config.App()
        self.bearer_token = app.config.get('Twitter', 'bearer_token')
        self.hashtag_search_url = app.config.get('Twitter', 'search_tweets_url')
        self.username_search_url = app.config.get('Twitter', 'search_author_url')

    def createAuthHeader(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers

    # delete soon
    def createSearchConditions(self, query, limit):
        data = {
            'max_results': limit,
            'query': query
        }
        return data

    def createSearchUrlHashtag(self, hashtag, limit):
        url = self.hashtag_search_url.format(hashtag) + "&count={}".format(limit)
        return url

    def getTweetsByHashtag(self, hashtag, limit=30):
        """
        Call Twitter API to get tweets by a single hashtag
        """
        auth_header = self.createAuthHeader()
        url = self.createSearchUrlHashtag(hashtag, limit)
        response = requests.get(url, headers=auth_header)
        if response.status_code != requests.codes.ok:
            print(url)
            raise Exception(response.status_code, response.text)
        return response.json()

    def createSearchUrlUsername(self, author):
        url = (self.base_url + self.separator + self.tweet_fields_author).format(author)
        return url

    def getTweetsByUsername(self, author, limit=30):
        """
        Call Twitter API to get tweets by username
        """
        auth_header = self.createAuthHeader()
        url = self.createSearchUrlUsername(author)
        response = requests.request("POST", url, headers=auth_header)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        # print(response.text)
        return response.json()

    def extractTweetInfo(self, tweet_result_json):
        """
        Extracts the relevant info from the Twitter API response
        """
        tweets = tweet_result_json['statuses']
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


# to delete
if __name__ == "__main__":
    twitter_api = TwitterApi()
    json_response = twitter_api.getTweetsByHashtag("%23kirby", 2)
    summary = twitter_api.extractTweetInfo(json_response)
    print(summary)
    print('success')
