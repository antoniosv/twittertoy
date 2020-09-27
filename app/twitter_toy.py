from flask import Flask, Blueprint
from twitter_api import TwitterApi

twitter_toy_blueprint = Blueprint('twitter_toy', __name__)

# routes


@twitter_toy_blueprint.route('/hashtags/<hashtag>')
def tweets_hashtag(hashtag):
    return hashtag
