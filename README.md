# twittertoy
get tweets from a tag or user name

## prerequisites

* python 3.6 or higher
* pip
* Twitter API token

## setup

1. put your Twitter API token inside ``./app/config/config.ini``, replacing the `bearer_token` default value.

2. launch virtual environment through your terminal:
``source ./twittertoy/.venv/Scripts/activate``

3. inside the virtual environment, run ``pip install -r requirements.txt``

## how to run

Run the flask container locally:

``python -m flask run``

Now you should see your local IP address and the port where the app was deployed, e.g.: 

``http://127.0.0.1:5000/``

## making requests

1. Get tweets by a hashtag:

``http://localhost:xxxx/hashtags/magic?limit=5``

2. Get tweets by a user name:

``http://localhost:xxxx/users/gandalf?limit=5``
