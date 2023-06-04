from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.sql import exists
import datetime as dt

# Create engine and reflect database tables
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Flask app
app = Flask(__name__)


# Create routes
@app.route("/")
def welcome():
    return f"""
        <html>
            <head>
                <title>Hawaii Weather API</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    
                    .route {{
                        margin: 10px 0;
                        padding: 10px;
                        background-color: #f0f0f0;
                        border-radius: 5px;
                    }}
                    
                    .route a {{
                        color: #333;
                        text-decoration: none;
                        font-weight: bold;
                    }}
                    
                    .route a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <h1>Hawaii Weather API</h1>
                <p>Here are the available routes:</p>
                <div class="route">
                    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
                    <p>Returns a JSON list of precipitation data for the last year.</p>
                </div>
                <div class="route">
                    <a href="/api/v1.0/stations">/api/v1.0/stations</a>
                    <p>Returns a JSON list of weather station names.</p>
                </div>
                <div class="route">
                    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
                    <p>Returns a JSON list of temperature observations for the last year.</p>
                </div>
                <div class="route">
                    <a href="/api/v1.0/&lt;start&gt;">/api/v1.0/&lt;start&gt;</a>
                    <p>Returns the minimum, maximum, and average temperature for all dates greater than or equal to the start date (in the format of YYYY-MM-DD).</p>
                </div>
                <div class="route">
                    <a href="/api/v1.0/&lt;start&gt;/&lt;end&gt;">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a>
                    <p>Returns the minimum, maximum, and average temperature for all dates between the start and end dates (in the format of YYYY-MM-DD/YYYY-MM-DD).</p>
                </div>
            </body>
        </html>
    """



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date).all()
    session.close()

    precipitation_data = []
    for date, tobs in results:
        precipitation_data.append({"date": date, "tobs": tobs})

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()

    stations_data = []
    for station, name in results:
        stations_data.append({"Station": station, "Name": name})

    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    query_date = dt.date(last_date.year -1, last_date.month, last_date.day)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()
    session.close()

    temp_data = []
    for date, tobs in results:
        temp_data.append({"date": date, "tobs": tobs})

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def start_only(start):
    session = Session(engine)
    date_range_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    date_range_min = session.query(Measurement.date).first()[0]
    valid_entry = session.query(exists().where(Measurement.date == start)).scalar()
    if valid_entry:
        results = (session.query(func.min(Measurement.tobs),
                     func.avg(Measurement.tobs),
                     func.max(Measurement.tobs))
                      .filter(Measurement.date >= start).all())
        tmin, tavg, tmax = results[0]
        result_printout = (['Entered Start Date: ' + start,
                            'The lowest Temperature was: '  + str(tmin) + ' F',
                            'The average Temperature was: ' + str(round(tavg, 1)) + ' F',
                            'The highest Temperature was: ' + str(tmax) + ' F'])
        return jsonify(result_printout)
    else:
        session.close()
        return jsonify({"error": f"Measurement data not available for the date {start}. Please enter a valid date between {date_range_min} and {date_range_max}."})

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    date_range_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    date_range_min = session.query(Measurement.date).first()[0]
    valid_entry_start = session.query(exists().where(Measurement.date == start)).scalar()
    valid_entry_end = session.query(exists().where(Measurement.date == end)).scalar()

    if valid_entry_start and valid_entry_end:
        results = (session.query(func.min(Measurement.tobs),
                     func.avg(Measurement.tobs),
                     func.max(Measurement.tobs))
                      .filter(Measurement.date >= start)
                      .filter(Measurement.date <= end)
                      .all())
        tmin, tavg, tmax = results[0]
        result_printout = (['Entered Start Date: ' + start + ' and End Date: ' + end,
                            'The lowest Temperature was: '  + str(tmin) + ' F',
                            'The average Temperature was: ' + str(round(tavg, 1)) + ' F',
                            'The highest Temperature was: ' + str(tmax) + ' F'])
        return jsonify(result_printout)
    else:
        session.close()
        if not valid_entry_start and not valid_entry_end:
            return jsonify({"error": f"Measurement data not available for the dates {start} and {end}. Please enter valid dates between {date_range_min} and {date_range_max}."})
        elif not valid_entry_start:
            return jsonify({"error": f"Measurement data not available for the date {start}. Please enter a valid start date between {date_range_min} and {date_range_max}."})
        elif not valid_entry_end:
            return jsonify({"error": f"Measurement data not available for the date {end}. Please enter a valid end date between {date_range_min} and {date_range_max}."})

if __name__ == '__main__':
    app.run()  # Add this line to run the application.
