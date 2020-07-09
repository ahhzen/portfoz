from flask import Flask, render_template, request, redirect, url_for
import pdb
import csv
import sys
import os
import pymongo
from datetime import datetime
import json
from functools import reduce

app = Flask(__name__)


@app.route("/")
def index():
    jsondata = open_json_file("index")
    if (jsondata):
        jsondata = jsondata.get("index")
        return render_template("index.html", data=jsondata)
    else:
        return "Something went wrong"

@app.route("/<string:page_name>")
def route_page(page_name, message=""):
    file, ext = page_name.split(".")
    jsondata = open_json_file(file)
    if (jsondata): 
        jsondata = jsondata.get(file)
        return render_template(page_name, anymessage = message, data=jsondata)
    else:
        return render_template(page_name, anymessage = message, data=None)


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


def open_json_file(filename):
    
    filename = filename + ".txt"
    filepath = os.path.join(os.getcwd(), "database", filename)

    try:
        string = ""
        with open(filepath, "r") as file:
            text = file.read()
            textlines = text.splitlines()
            
            for line in textlines:
                string += line
            file.close()
        
        data = json.loads(string)
        return data
    except:
        err = sys.exc_info()[0]
        print(f"Error: {err}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
