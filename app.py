#  import the Flask dependency.
from flask import Flask

# create a new flask app instance.
app = Flask(__name__)

# Create flask routes.
# Define the starting point - the root.
@app.route('/')

def hello_world():
    return 'Hello World'

