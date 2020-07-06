from flask import Flask, render_template, request, redirect, url_for
import pdb
import csv
import sys
import os
import pymongo
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<string:page_name>")
def route_page(page_name, message=""):
    return render_template(page_name, anymessage = message)


@app.route("/submitcontact", methods=["POST", "GET"])
def submitcontact():
    if request.method == "POST":
        try:
            # insertedid = store_contact(data)
            contactdata = request.form.to_dict()
            insertedid = store_contact_csv(contactdata)

            if insertedid and type(insertedid) == bool:
                message = "Thank You!"
                return render_template("contact.html", anymessage=message)
            else:
                message = insertedid
                return render_template("contact.html", anymessage=message)
        
        except:
            message = insertedid
            print("Error when retrieving data from request")
            return render_template("contact.html", anymessage = message)



def store_contact(data):
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["portfolio"]
        collection = db["contact"]

        result = collection.insert_one({"name": data.get("name"), "email": data.get("email"), "subject": data.get("subject"), "message": data.get("message")})
    except:
        return False
    else:
        return True


def store_contact_csv(data):
    try:
        with open("database/contact.csv", "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)

            timestamp = datetime.now().strftime("%d/%m/%Y-%X")
            csv_writer.writerow([data.get("name"), data.get("email"), data.get("subject"), data.get("message"), timestamp])
            csvfile.close()
    except:
        err = sys.exc_info()[0]
        message = f"Error: {err}"
        return message
    else:
        return True

if __name__ == "__main__":
    app.run(debug=True)
