import numpy as np
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists

from flask import Flask, jsonify, make_response

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
                <p>Enter a start date and an end date (YYYY-MM-DD) to get the minimum, maximum, and average temperature for the given range:</p>
                <form id="dateRangeForm">
                    <input type="text" id="startDate" name="startDate" placeholder="Start Date (YYYY-MM-DD)">
                    <input type="text" id="endDate" name="endDate" placeholder="End Date (YYYY-MM-DD)">
                    <button type="submit">Submit</button>
                </form>
                <p>Here are the available routes:</p>
                ...
            </body>
            <script>
                document.getElementById('dateRangeForm').addEventListener('submit', function(event) {{
                    event.preventDefault();
                    const startDate = document.getElementById('startDate').value;
                    const endDate = document.getElementById('endDate').value;
                    window.location.href = `/api/v1.0/${startDate}/${endDate}`;
                }});
            </script>
        </html>
    """



@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    session.close()

    precipitation_data = []
    for date, prcp in results:
        precipitation_data.append({"date": date, "prcp": prcp})

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name).all()
    station_details = list(np.ravel(results))
    return jsonify(station_details)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_start_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d') - dt.timedelta(days=365)
    q_station_list = (session.query(Measurement.station, func.count(Measurement.station))
                             .group_by(Measurement.station)
                             .order_by(func.count(Measurement.station).desc())
                             .all())
    station_hno = q_station_list[0][0]
    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs)
                      .filter(Measurement.date >= query_start_date)
                      .filter(Measurement.station == station_hno)
                      .all())
    tobs_list = [{"Date": row.date, "Station": row.station, "Temperature": row.tobs} for row in results]
    return jsonify(tobs_list)

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
        result = {
            "start_date": start,
            "lowest_temperature": f"{tmin} F",
            "average_temperature": f"{round(tavg, 1)} F",
            "highest_temperature": f"{tmax} F"
        }
        return jsonify(result)
    else:
        return jsonify({"error": f"Measurement data not available for the date {start}. Please enter a valid date between {date_range_min} and {date_range_max}."})


@app.route("/api/v1.0/<start>/<end>") 
def start_end(start, end):
    with Session(engine) as session:
        date_range_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
        date_range_min = session.query(Measurement.date).first()[0]

        try:
            start_date = dt.datetime.strptime(start, "%Y-%m-%d")
            end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": f"Invalid date format. Please use 'YYYY-MM-DD'."})

        if start_date <= end_date and date_range_min <= start_date.date() <= date_range_max and date_range_min <= end_date.date() <= date_range_max:
            results = (session.query(func.min(Measurement.tobs),
                                     func.avg(Measurement.tobs),
                                     func.max(Measurement.tobs))
                              .filter(Measurement.date >= start_date)
                              .filter(Measurement.date <= end_date).all())
            tmin, tavg, tmax = results[0]
            results_printout = (['Entered Start Date: ' + start,
                                'Entered End Date: ' + end,
                                'The lowest Temperature was: '  + str(tmin) + ' F',
                                'The average Temperature was: ' + str(round(tavg, 1)) + ' F',
                                'The highest Temperature was: ' + str(tmax) + ' F'])
            return jsonify(results_printout)
        else:
            return jsonify({"error": f"Measurement data not available for the given date range. Please enter valid dates between {date_range_min} and {date_range_max}."})



if __name__ == '__main__':
    app.run(debug=True)
