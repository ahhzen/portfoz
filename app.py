from flask import Flask, render_template, request
import csv
import sys
import os

app = Flask(__name__)

@app.route("/test")
def hello():
    return "Hello World"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def index2():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact1(message=None):
    return render_template("contact.html", anymessage = "")

@app.route("/works.html")
def works():
    return render_template("works.html")

@app.route("/work.html")
def work():
    return render_template("work.html")

@app.route("/components.html")
def components():
    return render_template("components.html")

@app.route("/submitcontact", methods=["POST", "GET"])
def submitcontact():
    if request.method == "POST":
        try:
            email = request.form.get("email", "No email")
            subject = request.form.get("subject", "No Subject")
            message = request.form.get("message", "No Message")
            # insertedid = store_contact(email, subject, message)
            contactdata = request.form.to_dict()
            insertedid = store_contact_csv(contactdata)

            if insertedid and type(insertedid) == bool:
                message = "Success!"
                return render_template("contact.html", anymessage=message)
##                return redirect(url_for("contact", message="Thank you for your message"))
            else:
                message = insertedid  #"Failed!"
                return render_template("contact.html", anymessage=message)
##                return redirect(url_for("contact", message="Something went wrong. Please try again later"))

        except:
            print("Error when retrieving data from request")


    return "Done"


# def store_contact(email, subject, message):
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client["portfolio"]
#     collection = db["contact"]

#     return collection.insert_one({"email": email, "subject": subject, "message": message})

def store_contact_csv(data):
    try:
        with open("./portfoz/database/contact.csv", "a") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
            email = data.get("email")
            subject= data.get("subject")
            message = data.get("message")

            csv_writer.writerow([email,subject,message])
            csvfile.close()

            return True
    except:
        err = sys.exc_info()[0]
        return "Error : %s " %err + os.getcwd()

if __name__ == "__main__":
    app.run()
