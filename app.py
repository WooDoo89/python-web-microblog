import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import urllib


def create_app():
    app = Flask(__name__)
    username = urllib.parse.quote_plus('vgurin')
    password = urllib.parse.quote_plus('Welcome@01')
    client = MongoClient(
        f"mongodb+srv://{username}:{password}@microblog.rrvd7jo.mongodb.net/test")
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(
                    entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
