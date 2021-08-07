from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_data
import pymongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/marsDB"
#mongo = PyMongo(app)

# Or set inline
#mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
client.drop_database("marsDB")
db = client.marsDB
marsCollection = db.marsNews

mdata = {}

@app.route("/")
def index():
    marsData = marsCollection.find_one()    
    return render_template("index.html", data=marsData)


@app.route("/scrape")
def scraper():
    mars_Data = scrape_data.scrape()       
    db.drop_collection("marsNews")
    marsCollection = db.marsNews
    marsCollection.insert(mars_Data)   
        
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
