from flask import Blueprint, request
from twitter_api import TwitterApi
import json

twitter_toy_blueprint = Blueprint('twitter_toy', __name__)

DEFAULT_LIMIT = 30

# routes


@twitter_toy_blueprint.route('/hashtags/<hashtag>/', methods=['GET'])
def tweets_hashtag(hashtag):
    limit = request.args.get('limit')
    if limit is None:
        limit = DEFAULT_LIMIT
    twitter_api = TwitterApi()
    json_response = twitter_api.getTweetsByHashtag(hashtag, limit)
    tweets = json_response['statuses']
    summary = twitter_api.extractTweetInfo(tweets)
    return json.dumps(summary)


@twitter_toy_blueprint.route('/users/<user>/', methods=['GET'])
def tweets_user(user):
    limit = request.args.get('limit')
    if limit is None:
        limit = DEFAULT_LIMIT
    twitter_api = TwitterApi()
    json_response = twitter_api.getTweetsByUsername(user, limit)
    summary = twitter_api.extractTweetInfo(json_response)
    return json.dumps(summary)
