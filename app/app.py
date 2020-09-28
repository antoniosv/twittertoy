from twitter_toy import twitter_toy_blueprint
from flask import Flask, make_response, jsonify

app = Flask(__name__)

# load blueprint

# register blueprint
app.register_blueprint(twitter_toy_blueprint)


@app.route("/")
def home():
    return "Hello, Flask!"
