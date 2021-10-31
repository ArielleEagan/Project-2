from flask import Flask, render_template

import datetime

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.ds_salaries

data = []
for dictionary in db.top5.find():
    d = {k:v for k,v in dictionary.items() if k != '_id'}
    temp_date = datetime.datetime.strftime(d['timestamp'], format='%Y-%m-%d')
    d['timestamp'] = temp_date
    data.append(d)


# Set route
@app.route('/')
def index():
    # Return the template with the teams list passed in
    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)