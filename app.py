import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
Station = Base.classes.station

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
        f'Available Routes:<br/>'
        f'<ul><li><a href="api/v1.0/precipitation">/api/v1.0/precipitation</a></li>'
        f'<li><a href="api/v1.0/stations">/api/v1.0/stations</a></li>'
        f'<li><a href="api/v1.0/tobs">/api/v1.0/tobs</a></li></ul><br/>'
        f'Start/End Date :<br/>'
        f"<ul><li>/api/v1.0/&lt;start&gt; </li>"
        f"<li>/api/v1.0/&lt;start&gt;/&lt;end&gt;</li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results =  session.query(Measurement.date, func.avg(Measurement.prcp)).group_by(Measurement.date).all()
    session.close()

    
    date_prcp = dict(results)

    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()


    stations = [x[0] for x in set(results)]
    station_dict = {"station_name":stations}

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519397").filter(Measurement.date >= '2016-08-24').all()
    session.close()

    tobs_dict = dict(results)
    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def stats1(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.tobs).filter(Measurement.date >= start ).all()

    session.close()

    TMIN = np.min([x[0] for x in results])
    TMAX = np.max([x[0] for x in results])
    TAVG = np.mean([x[0] for x in results])

    temp_dict = {'TMIN':TMIN,'TMAX':TMAX,'TAVG':TAVG}

    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>/<end>")
def stats2(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.tobs).filter(Measurement.date >= start ).filter(Measurement.date <= end).all()

    session.close()

    TMIN = np.min([x[0] for x in results])
    TMAX = np.max([x[0] for x in results])
    TAVG = np.mean([x[0] for x in results])

    temp_dict = {'TMIN':TMIN,'TMAX':TMAX,'TAVG':TAVG}

    return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)


