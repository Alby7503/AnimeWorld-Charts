from requests import get
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    with open("index.html", 'r') as f:
        return f.read()


@app.route("/search/<query>")
def search(query):
    return get("https://www.animeworld.tv/watchlist/" + query).text


app.run(debug=True)
