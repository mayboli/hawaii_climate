import numpy as np

import datetime as dt
from datetime import date
from datetime import time
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify

engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/%yyyy-%mm-%dd<br/>"
        f"/api/v1.0/%yyyy-%mm-%dd/%yyyy-%mm-%dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').\
        order_by(desc(Measurement.date)).all()
    
    all_precip = []
    for precip in results:
        precip_dict = {}
        precip_dict["date"] = precip.date
        precip_dict["precipitation"] = precip.prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()

    all_tobs = list(np.ravel(tobs))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    temps_start = list(np.ravel(results))
    
    return jsonify(temps_start)

@app.route("/api/v1.0/<start>/<end>")    
def start_end(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    temps_start_end = list(np.ravel(results))

    return jsonify(temps_start_end)

if __name__ == "__main__":
    app.run(debug=True)