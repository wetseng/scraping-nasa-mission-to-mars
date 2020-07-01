from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


import scrape_data

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


#################################################
# Flask Routes
#################################################

# /
# Home page.
# List all routes that are available.
@app.route("/")
def home():
    # Find the website data
    mars = mongo.db.mars_data.find_one()

    return render_template('index.html', mars=mars)
  

@app.route("/scrape")
def scraper():

    # Call scrape function in scrape_data.py and store in website_data
    mars = mongo.db.mars_data
    new_mars_data = scrape_data.scrape()

    # Update mongo db collection
    mars.update({}, new_mars_data, upsert=True) 

    # Redirect back to home /
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)