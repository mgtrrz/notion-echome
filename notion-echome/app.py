from json.encoder import JSONEncoder
from flask import Flask

app = Flask(__name__)

@app.route("/")
def front_page():
    return {}

@app.route("/update-notion")
def update_notion():
    from notion import update_notion
    return update_notion()