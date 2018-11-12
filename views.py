from datetime import datetime
from flask import abort, current_app, render_template

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def flights_page():
    db = current_app.config["db"]
    flights = db.get_flights()
    return render_template("flights.html", flights=sorted(flights))

def flight_page(flight_key):
    db = current_app.config["db"]
    flight = db.get_flight(flight_key)
    if flight is None:
        abort(404)
    return render_template("flight.html", flight=flight)
