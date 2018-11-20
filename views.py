from datetime import datetime
from flask import abort, current_app, render_template
from flask import request
from flask import redirect
from flask import url_for

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



def add_page():
    statement = """INSERT INTO COUNTRIES (country_name)
        VALUES (%(name)s)"""


    if request.method == "GET":
        return render_template("add_country.html")
    else:
        form_name = request.form["name"]
        
        try:
            connection = dbapi2.connect(dsn)
            cursor = connection.cursor()
            if (form_name):
                cursor.execute(statement, {'name': country_name})
            cursor.close()
            connection.close()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            return redirect(url_for("countries_page"))

def countries_page():
    statement = """SELECT country_id, country_name
        FROM COUNTRIES)"""
    data = ""
    try:
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        cursor.execute(statement)
        data = cursor.fetchall()
        for country_id, country_name in cursor:
            print('%(id)s: %(nm)s' % {'id': country_id, 'nm': country_name})
        cursor.close()
        connection.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
  
        return render_template("countries.html", data=sorted(data))
    
