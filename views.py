import os
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2

from flask import abort, current_app, render_template, flash
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user, login_user, logout_user
from psycopg2.tests import dsn

from flask import session

from forms import LoginForm
from user import get_user

def sqlgen_update(table_name, column_names, variables): #(string, list, list) !ID must be first item in lists. 
    command = "UPDATE " + table_name + " "
    for index in range(1,len(column_names)):#start from 1 to not change id
        if (variables[index] == "null"): 
            command += "SET " + column_names[index] + " = NULL, "         
        elif (variables[index] != ""):
            command += "SET " + column_names[index] + " = '" + variables[index] + "', "
    command = command[:-2] #remove last character (,) from string
    command += " WHERE " + column_names[0] + " = '" + variables[0] + "';"
    print("result: ")
    print(command)
    return command

def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.data["username"]
        user = get_user(username)
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def execute_sql(command):
    print("executing...")
    print(command)
    #command = """UPDATE COUNTRIES SET country_name = Turkey WHERE country_id = 1;"""
    try:
            url = "postgres://itucs:itucspw@localhost:32769/itucsdb"#url = os.getenv("DATABASE_URL")  #
            print("debug0")
            connection = dbapi2.connect(url)
            print("debug1")
            cursor = connection.cursor()
            print("debug2")
            cursor.execute(command)
            print("Execute works!")
            connection.commit()

    except dbapi2.DatabaseError:
            print("dataerror2")
            print(dbapi2.DatabaseError)
            connection.rollback()
            return -1;

    try:
            data = cursor.fetchall()
            cursor.close()
            connection.close()

    except dbapi2.DatabaseError:
            print("dataerror3")
            print(dbapi2.DatabaseError)
            connection.rollback()
            return -2;

    return data

@login_required
def admin_page():
    if not current_user.is_admin:
        abort(401)
    return render_template("admin_page.html")

@login_required
def admin_select_table():
    if not current_user.is_admin:
        abort(401)
    command = request.args.get('command')
    if request.method == "GET":
        return render_template("admin_select_table.html")
    if request.method == "POST":
        table_name = request.form['table']
        
        session['table'] = table_name # store parameter in cookie

        #new_url = "/admin_page/" + command 
        if (command == "add"):
            return redirect(url_for("admin_add_page"))  #change to admin_add_page
        elif (command == "delete"):
            return redirect(url_for("admin_delete_page"))
        elif (command == "update"):
            return redirect(url_for("admin_update_page"))
        elif (command == "view"):
            return redirect(url_for("admin_view_page"))
        elif (command == "sql"):
            return redirect(url_for("admin_sql_page"))    
        else:
            print("error1")
            return redirect(url_for("admin_page"))  

@login_required
def admin_add_page():
    if not current_user.is_admin:
        abort(401)

    my_table = session['table']  # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    print(my_table)
    if request.method == "GET":
        return render_template("admin_add_page.html", table=my_table)

    if request.method == "POST":
        command = ""  # write code to generate update based on number of non-empty inputs and table name
        if (my_table == 'PASSENGERS'):

            country_id = request.form['country_id']
            passenger_name = request.form['passenger_name']
            passenger_last_name = request.form['passenger_last_name']
            number_of_flights = request.form['number_of_flights']
            last_flight_date = request.form['last_flight_date']
            email = request.form['email']
            if (country_id == '' or passenger_name == '' or passenger_last_name == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO PASSENGERS (country_id, passenger_name, passenger_last_name)
                         VALUES (%(country_id)s,
                                 '%(passenger_name)s',
                                 '%(passenger_last_name)s');"""


            data = execute_sql(command % {'country_id': country_id, 'passenger_name': passenger_name, 'passenger_last_name': passenger_last_name})
            print(data)

        elif (my_table == 'FLIGHTS'):
            aircraft_id = request.form['aircraft_id']
            print(aircraft_id)
            route_id = request.form['route_id']
            staff_id = request.form['staff_id']
            departure_date = request.form['departure_date']

            arrival_date = request.form['arrival_date']
            number_of_passengers = request.form['number_of_passengers']
            duration = request.form['duration']
            number_of_staff = request.form['number_of_staff']
            if (aircraft_id == '' or route_id == '' or staff_id == '' or departure_date == '' or arrival_date == '' or number_of_passengers == '' or duration == '' or number_of_staff == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO FLIGHTS (aircraft_id, route_id, staff_id, departure_date, arrival_date, number_of_passengers, duration, number_of_staff)
                         VALUES (%(aircraft_id)s,
                                 %(route_id)s,
                                 %(staff_id)s,
                                 '%(departure_date)s',
                                 '%(arrival_date)s',
                                 %(number_of_passengers)s,
                                 %(duration)s,
                                 %(number_of_staff)s);"""


            data = execute_sql(command % {'aircraft_id': aircraft_id, 'route_id': route_id, 'staff_id': staff_id, 'departure_date': departure_date, 'arrival_date': arrival_date, 'number_of_passengers': number_of_passengers, 'duration': duration, 'number_of_staff': number_of_staff})
            print(data)

        elif (my_table == 'BOOKINGS'):
            flight_id = request.form['flight_id']
            print(flight_id)

            passenger_id = request.form['passenger_id']

            payment_type = request.form['payment_type']

            miles_used = request.form['miles_used']
            seat = request.form['seat']

            class_of_seat = request.form['class']
            fare = request.form['fare']
            if (flight_id == '' or passenger_id == '' or payment_type == '' or miles_used == '' or seat == '' or class_of_seat == '' or fare == ''  ):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO BOOKINGS (flight_id, passenger_id, payment_type, miles_used, seat, class_of_seat, fare)
                         VALUES (%(flight_id)s,
                                 %(passenger_id)s,
                                 '%(payment_type)s',
                                 %(miles_used)s,
                                 '%(seat)s',
                                 '%(class_of_seat)s',
                                 %(fare)s);"""


            data = execute_sql(command % { 'flight_id': flight_id, 'passenger_id': passenger_id, 'payment_type': payment_type, 'miles_used': miles_used, 'seat': seat, 'class_of_seat': class_of_seat, 'fare': fare})
            print(data)


        elif (my_table == 'AIRCRAFTS'):
            airline_id = request.form['airline_id']

            capacity = request.form['capacity']

            company_name = request.form['company_name']

            model_name = request.form['model_name']
            maximum_range = request.form['maximum_range']

            year_produced = request.form['year_produced']

            if (airline_id == '' or capacity == '' or company_name == '' or model_name == '' or maximum_range == '' or year_produced == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range, year_produced)
                         VALUES (%(airline_id)s,
                                 %(capacity)s,
                                 '%(company_name)s',
                                 '%(model_name)s',
                                 %(maximum_range)s,
                                 %(year_produced)s);"""


            data = execute_sql(command % { 'airline_id': airline_id, 'capacity': capacity, 'company_name': company_name, 'model_name': model_name, 'maximum_range': maximum_range, 'year_produced': year_produced})
            print(data)

        elif (my_table == 'ROUTES'):
            dep_airport_id = request.form['dep_airport_id']

            arr_airport_id = request.form['arr_airport_id']

            route_name = request.form['route_name']

            distance = request.form['distance']
            number_of_airlines = request.form['number_of_airlines']

            if (dep_airport_id == '' or arr_airport_id == '' or route_name == '' or distance == '' or number_of_airlines == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance, number_of_airlines)
                         VALUES (%(dep_airport_id)s,
                                 %(arr_airport_id)s,
                                 '%(route_name)s',
                                 %(distance)s,
                                 %(number_of_airlines)s);"""


            data = execute_sql(command % { 'dep_airport_id': dep_airport_id, 'arr_airport_id': arr_airport_id, 'route_name': route_name, 'distance': distance, 'number_of_airlines': number_of_airlines})
            print(data)

        elif (my_table == 'STAFF'):
            country_id = request.form['country_id']

            airline_id = request.form['airline_id']

            job_title = request.form['job_title']

            staff_name = request.form['staff_name']
            staff_last_name = request.form['staff_last_name']

            start_date = request.form['start_date']


            if (country_id == '' or airline_id == '' or job_title == '' or staff_name == '' or staff_last_name == '' or start_date == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date)
                         VALUES (%(country_id)s,
                                 %(airline_id)s,
                                 '%(job_title)s',
                                 '%(staff_name)s',
                                 '%(staff_last_name)s',
                                 '%(start_date)s');"""


            data = execute_sql(command % { 'country_id': country_id, 'airline_id': airline_id, 'job_title': job_title, 'staff_name': staff_name, 'staff_last_name': staff_last_name, 'start_date': start_date})
            print(data)

        return redirect(url_for("admin_page"))

@login_required
def admin_delete_page():
    if not current_user.is_admin:
        abort(401)
    my_table = session['table']  # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    print(my_table)
    if request.method == "GET":
        return render_template("admin_delete_page.html", table=my_table)

    if request.method == "POST":
        command = ""  # write code to generate update based on number of non-empty inputs and table name
        if (my_table == 'PASSENGERS'):
            passenger_id = request.form['passenger_id']
            if (passenger_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """DELETE FROM PASSENGERS 
                        WHERE passenger_id = %(name)s"""


            data = execute_sql(command % {'name': passenger_id})



        elif (my_table == 'FLIGHTS'):
            flight_id = request.form['flight_id']

            if (flight_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM FLIGHTS 
                             WHERE flight_id = %(name)s"""

            data = execute_sql(command % {'name': flight_id})

        elif (my_table == 'BOOKINGS'):
            flight_id = request.form['flight_id']
            passenger_id = request.form['passenger_id']

            if (flight_id == '' or passenger_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM BOOKINGS 
                             WHERE (flight_id = %(flight_id)s) and (passenger_id = %(passenger_id)s)"""

            data = execute_sql(command % {'flight_id': flight_id, 'passenger_id': passenger_id})

        elif (my_table == 'AIRCRAFTS'):
            aircraft_id = request.form['aircraft_id']

            if (aircraft_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM AIRCRAFTS 
                             WHERE aircraft_id = %(name)s"""

            data = execute_sql(command % {'name': aircraft_id})

        elif (my_table == 'ROUTES'):
            route_id = request.form['route_id']

            if (route_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM ROUTES 
                             WHERE route_id = %(name)s"""

            data = execute_sql(command % {'name': route_id})

        elif (my_table == 'STAFF'):
            staff_id = request.form['staff_id']

            if (staff_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM STAFF 
                             WHERE staff_id = %(name)s"""

            data = execute_sql(command % {'name': staff_id})



        return redirect(url_for("admin_page"))  # change this into a page that displays whether operation was successful or not


@login_required
def admin_update_page():
    if not current_user.is_admin:
        abort(401)
    my_table = session['table']       # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    print(my_table)
    if request.method == "GET":
        return render_template("admin_update_page.html", table = my_table)


    if request.method == "POST":
     #write code to generate update based on number of non-empty inputs and table name
        if (my_table == 'COUNTRIES'):
            country_name = request.form['country_name']
            country_id = request.form['country_id']
            
            if (country_id == '' or country_name == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_update_page"))
            #rewrite command so that empty forms do not change during the update command
            #command = """UPDATE COUNTRIES 
            #            SET country_name = '%(name)s'  
            #           WHERE country_id = %(id)s;"""
            command = sqlgen_update("COUNTRIES", ["country_id", "country_name"] ,[country_id, country_name])
            
            data = execute_sql(command)




        elif (my_table == 'AIRCRAFTS'):
            aircraft_name = request.form['aircraft_name']
            aircraft_id = request.form['aircraft_id']
            if (aircraft_id == '' or aircraft_name == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_update_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """UPDATE AIRCRAFTS 
                        SET aircraft_name = '%(name)s'  
                        WHERE aircraft_id = %(id)s;"""

            data = execute_sql(command % {'name': aircraft_name, 'id': aircraft_id})



        return redirect(url_for("admin_page"))  # change this into a page that displays whether operation was successful or not

@login_required
def admin_view_page():
    if not current_user.is_admin:
        abort(401)
    my_table = session['table']  # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    print(my_table)
    if request.method == "GET":
        command = """SELECT * FROM 
                          %(name)s;"""

        data = execute_sql(command % {'name': my_table})

        return render_template("admin_view_page.html", table=my_table, data=sorted(data))







