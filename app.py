# Entry point for the application.
import json
import renderer
from random import randint
import uuid
from datetime import datetime
import os
from flask import Flask,render_template, make_response
app = Flask(__name__)


@app.route("/")
def home():
    pagename = getCategory_List()
    return pagename

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/getCategoryList/")
def getCategory_List():
    #return the list

    #FIND LIST
    datatoinput = ""
    with open("static/data/categories.json","r") as file:
                jsonData = json.load(file)
                for categories in jsonData:
                    print("Category: ", categories["name"])
                    if categories["available"]:
                        datatoinput = datatoinput + "<li><a href='getJeopardyQuestions/" + categories["csv_file"] +"'>" + categories["name"] + "</a></li>"
                    else:
                        datatoinput = datatoinput + "<li>" + categories["name"] + " (CURRENTLY NOT AVAILABLE)</li>"
    #OPEN TEMPLATE FILE
    with open('templates/home.html', 'r') as f:
        text = f.read()

    #REPLACE WITH LIST DATA
    text = text.replace("[REPLACE]", datatoinput)

    #CREATE UNIQUE PAGE
    pageid = uuid.uuid4()
    pageid_string = str(pageid)
    with open('templates/home_' + pageid_string + ".html", 'w') as fi:
        fi.write(text)

    #CREATE RESPONSE
    resp = make_response(render_template('home_' + pageid_string + ".html"))
    #resp.mimetype = 'text/plain'

    #DELETE UNIQUE PAGE
    if os.path.exists('templates/home_' + pageid_string + ".html"):
        os.remove('templates/home_' + pageid_string + ".html")
    else:
        print("The file does not exist")

    #RETURN RESPONSE
    return resp

@app.route("/getJeopardyQuestions/<category>")
def getJeopardy_Questions(category):
    pageid = uuid.uuid4()
    pageid_string = str(pageid)
    #OpenFile
    f = 'static/data/' + category + '.csv'
    renderer.make_jeopardy(f,pageid_string)
    
    resp = make_response(render_template("jeopardy_" + pageid_string + ".html"))
    #DELETE UNIQUE PAGE
    if os.path.exists("templates/jeopardy_" + pageid_string + ".html"):
        os.remove("templates/jeopardy_" + pageid_string + ".html")
    else:
        print("The file does not exist")

    #RETURN RESPONSE
    return resp

''' @app.route("/api/data")
def get_data():
    return app.send_static_file("data.json") '''

''' @app.route("/api/QuoteoftheDay")
def random_question():
    with open('static/data/data.json') as quotesfile:
        data = json.load(quotesfile)
        qs = data["quotes"]
        random_index = randint(0, len(qs)-1)
        return qs[random_index] '''


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
