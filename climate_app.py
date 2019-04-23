import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"/api/< start ></br>"
        f"/api/< start >/< end ></br>"
    )

#################################################
# Precipitation
#################################################

@app.route("/api/precipitation")
def precipitation():
    """Return a list of all precipitation data"""
    
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).\
    order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

#################################################
# Stations
#################################################

@app.route("/api/stations")
def station():
    """Returns all stations in Hawaii"""
    station_data = session.query(Station.station)
    station_list = []
    for station in station_data:
        station_dict = {}
        station_dict['station'] = station
        station_list.append(station_dict)
    return jsonify(station_list)


#################################################
# Temperature
#################################################

@app.route("/api/temperature")
def temperature():
    """Return a list of temperatures for prior year"""
# Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

    temp_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= dt.date(2017, 8, 23) - dt.timedelta(days=365)).\
        order_by(Measurement.date).all()
# Create a list of dicts with `date` and `tobs` as the keys and values
    temp_list = []
    for date, tobs in temp_data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)


#################################################
# Dates TMIN, TAVG, TMAX
#################################################


@app.route("/api/<start>")
def start_trip(start):
#query trip data
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    trip= {"START DATE":start, "TMIN":trip_data[0][0], "TAVG":trip_data[0][1], "TMAX":trip_data[0][2]}
    return jsonify(trip)

@app.route("/api/<start>/<end>")
def startend_trip(start,end):
 
 # query trip data  
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    trip= {"START DATE":start, "END DATE": end, "TMIN":trip_data[0][0], "TAVG":trip_data[0][1], "TMAX":trip_data[0][2]}
    return jsonify(trip)    


if __name__ == '__main__':
    app.run(debug=True)