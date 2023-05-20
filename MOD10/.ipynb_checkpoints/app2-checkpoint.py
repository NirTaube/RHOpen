{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "247933ef",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import re\n",
    "import datetime as dt\n",
    "import sqlalchemy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "d8ac38df",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from sqlalchemy.sql import exists  \n",
    "\n",
    "from flask import Flask, jsonify\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "933d89f5",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create engine and reflect database tables\n",
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "b95eb9f8",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create Flask app\n",
    "app = Flask(__name__)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "f0f91482",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create routes\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/start (enter as YYYY-MM-DD)<br/>\"\n",
    "        f\"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)\"\n",
    "    )\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def precipitation():\n",
    "    session = Session(engine)\n",
    "    results = (session.query(Measurement.date, Measurement.tobs)\n",
    "                      .order_by(Measurement.date))\n",
    "    precipitation_date_tobs = [{\"date\": row.date, \"tobs\": row.tobs} for row in results]\n",
    "    return jsonify(precipitation_date_tobs)\n",
    "\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    session = Session(engine)\n",
    "    results = session.query(Station.name).all()\n",
    "    station_details = list(np.ravel(results))\n",
    "    return jsonify(station_details)\n",
    "\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    session = Session(engine)\n",
    "    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()\n",
    "    query_start_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d') - dt.timedelta(days=365)\n",
    "    q_station_list = (session.query(Measurement.station, func.count(Measurement.station))\n",
    "                             .group_by(Measurement.station)\n",
    "                             .order_by(func.count(Measurement.station).desc())\n",
    "                             .all())\n",
    "    station_hno = q_station_list[0][0]\n",
    "    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs)\n",
    "                      .filter(Measurement.date >= query_start_date)\n",
    "                      .filter(Measurement.station == station_hno)\n",
    "                      .all())\n",
    "    tobs_list = [{\"Date\": row.date, \"Station\": row.station, \"Temperature\": row.tobs} for row in results]\n",
    "    return jsonify(tobs_list)\n",
    "\n",
    "@app.route(\"/api/v1.0/<start>\") \n",
    "def start_only(start):\n",
    "    session = Session(engine)\n",
    "    date_range_max = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]\n",
    "    date_range_min = session.query(Measurement.date).first()[0]\n",
    "    valid_entry = session.query(exists().where(Measurement.date == start)).scalar()\n",
    "    if valid_entry:\n",
    "    \tresults = (session.query(func.min(Measurement.tobs),\n",
    "    \t\t\t\t func.avg(Measurement.tobs),\n",
    "    \t\t\t\t func.max(Measurement.tobs))\n",
    "    \t\t\t\t  .filter(Measurement.date >= start).all())\n",
    "    \ttmin, tavg, tmax = results[0]\n",
    "    \tresult_printout = (['Entered Start Date: ' + start,\n",
    "    \t\t\t\t\t\t'The lowest Temperature was: '  + str(tmin) + ' F',\n",
    "    \t\t\t\t\t\t'The average Temperature was: ' + str(round(tavg, 1)) + ' F',\n",
    "    \t\t\t\t\t\t'The highest Temperature was: ' + str(tmax) + ' F'])\n",
    "    \treturn jsonify(result_printout)\n",
    "    else:\n",
    "    \treturn jsonify({\"error\": f\"Measurement data not available for the date {start}. Please enter a valid date between {date_range_min} and {date_range_max}.\"})\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b3a6b509",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Conda",
   "language": "python",
   "name": "anaconda"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.16"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}