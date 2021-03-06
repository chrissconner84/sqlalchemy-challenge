# 1. import Flask
from flask import Flask, jsonify

import datetime as dt
import numpy as np
#import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect,desc

app = Flask(__name__)
#database_path = "Resources/hawaii.sqlite"
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base=automap_base()
base.prepare(engine, reflect=True)
print (base.classes.keys())
Measurement=base.classes.measurement
Station=base.classes.station
session=Session(engine)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start -- Please enter start date in yyyy-mm-dd format within quotes<br/>"
        f"/api/v1.0/start/end -- Please enter starte date in yyy-mm-dd format within quotes followed by \ then enter end date\
        in yyy-mm-dd format within quotes"
    )



@app.route("/api/v1.0/percipitation")
def percip():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= query_date).all()
    # Convert list of tuples into normal list
    results2= list(np.ravel(results))
    return jsonify(results2)
    
    session.close()

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station_list = session.query(Station.id,Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    station_list2= list(np.ravel(station_list))
    return jsonify (station_list2)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)    
    tobs_list=session.query(Measurement.tobs,Measurement.date).filter(Measurement.station=='USC00519281')\
    .filter(Measurement.date>='2016-08-23').all()
    tobs_list2= list(np.ravel(tobs_list))
    return jsonify(tobs_list2)
    session.close()

@app.route("/api/v1.0/<sd>")
def start(sd):
     session = Session(engine)
     st= session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs).filter(Measurement.date >=sd)).all()
     st2= list(np.ravel(st))
     return jsonify(st2)

@app.route("/api/v1.0/<sd>/<ed>")
def start_end(sd,ed):
     session = Session(engine)
     se= session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs).filter(Measurement.date >= sd).filter(Measurement.date <= ed)).all()
     se2= list(np.ravel(se))
     return jsonify(se2)
     session.close()

if __name__ == "__main__":
    app.run(debug=True)
