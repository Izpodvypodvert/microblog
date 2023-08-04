import os
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    SERVER = os.getenv('SERVER')
    client = MongoClient(
        f"mongodb+srv://{USERNAME}:{PASSWORD}@{SERVER}.mongodb.net/microblog")

    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
