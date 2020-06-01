from flask import Flask, redirect, url_for, render_template, request, session
from flask_cachebuster import CacheBuster
from flask_pymongo import PyMongo, pymongo
from datetime import timedelta, datetime
import pprint
import json
import os

print = pprint.pprint

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dziennik-ministrancki-dev"

config = { 'extensions': ['.js', '.css', '.csv'], 'hash_size': 5 }
cache_buster = CacheBuster(config=config)
cache_buster.init_app(app)

mongo = PyMongo(app)
db = mongo.db


@app.route('/')
def main_page():
    ministranci = db.uzytkownicy.find()
    return render_template("index.html", ministranci=ministranci)


@app.route('/ministrant', methods=["POST", "GET"])
def dodaj_ministranta():
    if request.method == "POST":
        db.uzytkownicy.insert_one({
            "imie": request.form["imie"],
            "nazwisko": request.form["nazwisko"],
            "rola": "ministrant"
        })
        return redirect(url_for("main_page"))



@app.route('/msze', methods=["POST", "GET"])
def dodaj_msze():
    if request.method == "GET":
        db.msze.insert_one({
            "dzien_tygodnia": request.form["dzien_tygodnia"],
            "godzina": request.form["godzina"],
        })


if __name__ == '__main__':
    app.run()
