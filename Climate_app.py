 # Ignore SQLITE warnings related to Decimal numbers in the Chinook database
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of your dictionary."""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    all_precipitation=[]
    for precip in results:
        precip_dict = {}
        precip_dict["date"] = precip.date
        precip_dict["prcp"] = precip.prcp
        all_precipitation.append(precip_dict)

    return jsonify(all_precipitation)
	
@app.route("/api/v1.0/stations")
def stations():
    """Return the JSON representation of your dictionary."""
    # Query list of stations and counts
    results = session.query(Measurement.station, func.count(Measurement.station)).\
                group_by(Measurement.station).\
                order_by(func.count(Measurement.station).desc()).all()

    # Convert the query results to a list of stations inside Dicitonary
    all_stations=[]
    for row in results:
        station_dict = {}
        station_dict["station"] = row[0]
        station_dict["count"] = row[1]
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the JSON representation of your dictionary."""
    last_date=session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    for date in last_date:
        split_last_date=date.split('-')
    
    last_year=int(split_last_date[0])
    last_month=int(split_last_date[1])
    last_day=int(split_last_date[2])
    
    query_date = dt.date(last_year, last_month, last_day) - dt.timedelta(days=365)
    
    # Query list of stations and counts
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date>=query_date).\
                order_by(Measurement.date).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    last_12months_tobs=[]
    for row in results:
        tobs_dict = {}
        tobs_dict["date"] = row.date
        tobs_dict["station"] = row.tobs
        last_12months_tobs.append(tobs_dict)

    return jsonify(last_12months_tobs)

