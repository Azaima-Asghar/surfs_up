# SET UP THE FLASK WEATHER APP.

# Import Dependencies.
import datetime as dt
import numpy as np 
import pandas as pd 

# Import Dependencies Needed For SQLAlchemy.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Dependencies Needed For Flask.
from flask import Flask, jsonify

# Set up the database engine for flask application.
engine = create_engine('sqlite:///hawaii.sqlite')

# Reflect the database into classes.
Base = automap_base()
Base.prepare(engine, reflect = True)

# Save references to each table.
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create a link for session.
session = Session(engine)

# create a new flask app instance.
app = Flask(__name__)

# Create flask routes.

# Define the starting point - the root.
@app.route('/')

# Create a welcome function for root route.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br>
    Available Routes: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/temp/start/end
    ''')

# Create route for the precipitation analysis.
@app.route('/api/v1.0/precipitation')

# Create function for the precipitation analysis.
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    # use jsonify() to format our results into a JSON structured file.
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create route for stations.
@app.route('/api/v1.0/stations')

# Create a fuction for stations.
def stations():
    results = session.query(Station.station).all()
    # We want to start by unraveling our results into a one-dimensional array.
    stations = list(np.ravel(results))
    return jsonify(stations)

# Create route for temperature observations.
@app.route('/api/v1.0/tobs')

# Create fuction for temperature observations.
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # Unravel the results into a one-dimensional array and convert that array into a list.
    temps = list(np.ravel(results))
    return jsonify(temps)

 # Create route for statistics.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a fuction for statistics route.
def stats(start = None, end= None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
           filter(Measurement.date >= start).\
	     filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)
