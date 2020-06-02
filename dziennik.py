from flask import Flask, redirect, url_for, render_template, request, session
from flask_cachebuster import CacheBuster
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
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


@app.route('/msza', methods=["POST", "GET"])
def dodaj_msza():
    msze = db.msze.find()
    if request.method == "POST":
        db.msze.insert_one({
            "dzien_tygodnia": request.form["dzien_tygodnia"],
            "godzina": request.form["godzina"],
        })
    return render_template("msze.html", msze=msze)


@app.route('/sluzba', methods=["POST", "GET"])
def dodaj_sluzba():
    ministranci = db.uzytkownicy.find()
    msze = db.msze.find()
    sluzby = db.sluzby.find()
    sluzby_display = [
        {
            "ministrant": db.uzytkownicy.find_one({"_id": ObjectId(sluzba["ministrant_id"])})["imie"] + " " + db.uzytkownicy.find_one({"_id": ObjectId(sluzba["ministrant_id"])})["nazwisko"],
            "msza": db.msze.find_one({"_id": ObjectId(sluzba["msza_id"])})["dzien_tygodnia"] + " " + db.msze.find_one({"_id": ObjectId(sluzba["msza_id"])})["godzina"]
        }
        for sluzba in sluzby
    ]
    if request.method == "POST":
        # rozwiazanie na duplikaty
        doc = {"ministrant_id": request.form["ministrant"], "msza_id": request.form["msza"]}
        db.sluzby.update_one(doc, {"$set":doc}, upsert=True)
        # OLD SOLUTION
        # db.sluzby.insert_one({
        #     "ministrant_id": request.form["ministrant"],
        #     "msza_id": request.form["msza"]
        # })
    return render_template("sluzby.html", ministranci=ministranci, msze=msze, sluzby=sluzby_display)


@app.route('/obecnosc', methods=["POST", "GET"])
def dodaj_obecnosc():
    ministranci = db.uzytkownicy.find()
    msze = db.msze.find()
    obecnosci = db.obecnosci.find()
    obecnosci_display = [
        {
            "ministrant": db.uzytkownicy.find_one({"_id": ObjectId(obecnosc["ministrant_id"])})["imie"] + " " + db.uzytkownicy.find_one({"_id": ObjectId(obecnosc["ministrant_id"])})["nazwisko"],
            "msza": db.msze.find_one({"_id": ObjectId(obecnosc["msza_id"])})["dzien_tygodnia"] + " " + db.msze.find_one({"_id": ObjectId(obecnosc["msza_id"])})["godzina"]
        }
        for obecnosc in obecnosci
    ]
    if request.method == "POST":
        db.obecnosci.insert_one({
            "ministrant_id": request.form["ministrant"],
            "msza_id": request.form["msza"]
        })
    return render_template("obecnosci.html", ministranci=ministranci, msze=msze, obecnosci=obecnosci_display)

if __name__ == '__main__':
    # db.uzytkownicy.remove()
    # db.msze.remove()
    # db.sluzby.remove()
    # db.obecnosci.remove()
    app.run()
