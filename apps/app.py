# Import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

# Setting up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up App Routes
# Define the route to the HTML page
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html", mars=mars)
# Scrape the info
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

# Running Flask
if __name__ == "__main__":
    app.run()
