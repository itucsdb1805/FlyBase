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
from user import get_user, execute_sql

def sqlgen_update(table_name, column_names, variables, primary_key_count): #(string, list, list) !ID must be first item in lists. 
    command = "UPDATE " + table_name + " " + " SET "
    for index in range(primary_key_count,len(column_names)):#start from id_count in order to not change id
        if (variables[index] == "null"): 
            command += column_names[index] + " = NULL, "
        elif (variables[index] != ""):
            command += column_names[index] + " = '" + variables[index] + "', "
    command = command[:-2] #remove last character (,) from string
    if (primary_key_count == 1):
        command += " WHERE " + column_names[0] + " = '" + variables[0] + "';"
    elif (primary_key_count == 2):
        command += " WHERE " + column_names[0] + " = '" + variables[0] + "' AND " + column_names[1] + " = '" + variables[1] + "';"
    else:
        print("error primary_id_count must be 1 or 2")
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
            departure_date = request.form['departure_date']

            arrival_date = request.form['arrival_date']
            fuel_consumption = request.form['fuel_consumption']
            duration = request.form['duration']
            average_altitude = request.form['average_altitude']
            if (aircraft_id == '' or route_id == ''  or departure_date == '' or arrival_date == '' or fuel_consumption == '' or duration == '' or average_altitude == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO FLIGHTS (aircraft_id, route_id, staff_id, departure_date, arrival_date, fuel_consumption, duration, average_altitude)
                         VALUES (%(aircraft_id)s,
                                 %(route_id)s,
                                 '%(departure_date)s',
                                 '%(arrival_date)s',
                                 %(fuel_consumption)s,
                                 %(duration)s,
                                 %(average_altitude)s);"""


            data = execute_sql(command % {'aircraft_id': aircraft_id, 'route_id': route_id, 'departure_date': departure_date, 'arrival_date': arrival_date, 'fuel_consumption': fuel_consumption, 'duration': duration, 'average_altitude': average_altitude})
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
        command = ""     #write code to generate update based on number of non-empty inputs and table name
        #if (my_table == 'COUNTRIES'):
         #   new_name = request.form['country_name']
         #   new_id = request.form['country_id']
         #   table_name = "COUNTRIES"
        #    command = sqlgen_update(table_name, ["country_id", "country_name"], [new_name, new_id])
        primary_key_count = 1; #counts how many primary keys there are, all main tables, except bookings, have one primary id
        if (my_table == 'PASSENGERS'):
            table_name = "PASSENGERS"
            values = [request.form['passenger_id'], request.form["email"], request.form["country_id"], request.form["name"], request.form["middlename"],               request.form["surname"], request.form["passport_id"] ,request.form["photograph"], request.form[gender]]
            column_names = ["passenger_id", "email", "country_id", "passenger_name", "passenger_middle_name", "passenger_last_name", "passport_id" ,"photograph", "gender" ]
        elif (my_table == 'STAFF'):
            table_name = "STAFF"
            values = [request.form["staff_id"], request.form["country_id"], request.form["airline_id"], request.form["job_title"], request.form["name"], request.form["surname"], request.form["start_date"], request.form["fotograph"], request.form[gender]] 
            column_names = ["staff_id", "country_id", "airline_id", "job_title", "staff_name", "staff_last_name", "start_date", "fotograph", "gender" ]
        elif (my_table == 'BOOKINGS'):
            table_name = "BOOKINGS"
            primary_key_count = 2
            values = [request.form["booking_id"], request.form["flight_id"], request.form["passenger_id"], request.form["payment_type"],request.form["seat_number"], request.form["class_type"], request.form["fare"]]
            column_names = ["booking_id", "flight_id", "passenger_id", "payment_type", "seat_number", "class_type", "fare"]
        elif (my_table == 'FLIGHTS'):
            table_name = "FLIGHTS"
            values = [request.form["flight_id"], request.form["aircraft_id"], request.form["route_id"], request.form["departure_date"], request.form["arrival_date"], request.form["fuel_consumption"], request.form["duration"], request.form["average_altitude"]]
            column_names = ["flight_id", "aircraft_id", "route_id", "departure_date", "arrival_date", "fuel_consumption", "duration", "averge altitude"]
        elif (my_table == 'AIRCRAFTS'):
            table_name = "AIRCRAFTS"  
            values = [request.form["aircraft_id"], request.form["airline_id"],request.form["capacity"], request.form["company_name"],request.form["model_name"], request.form["maximum_range"], request.form["year_produced"]]
            column_names =  ["aircraft_id", "airline_id","capacity", "company_name", "model_name", "maximum_range", "year_produced"]      
        elif (my_table == 'ROUTES'):
            table_name = "ROUTES"  
            values = [request.form["route_id"], request.form["dep_airport_id"], request.form["arr_airport_id"], request.form["route_name"], request.form["distance"], request.form["number_of_airlines"], request.form["altitude"]]
            column_names = ["route_id", "dep_airport_id", "arr_airport_id", "route_name", "distance", "number_of_airlines", "altitude"]  

        command = sqlgen_update(table_name, column_names, values, primary_key_count)
        execute_sql(command)
        return redirect(url_for("admin_page")) #change this into a page that displays whether operation was successful or not

@login_required
def admin_view_page():
    if not current_user.is_admin:
        abort(401)
    my_table = session['table']  # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    if request.method == "GET":
        command = """SELECT * FROM %(name)s;"""

        data = execute_sql(command % {'name': my_table})
        data[1:] = sorted(data[1:])
        return render_template("admin_view_page.html", table=my_table, data=data)

def admin_sql_page():
    if not current_user.is_admin:
        abort(401)
    my_table = session['table']  # get table from session cookie, defined in admin_select_table()
    if (my_table == ""):
        abort(401)
    if request.method == "GET":
        return render_template("admin_sql_page.html")
    elif request.method == "POST":
        print("debug")
        command = request.form["command"]
        data = execute_sql(command)
        data[1:] = sorted(data[1:])
        return render_template("admin_view_page.html", data = data)

def register_page():
    if request.method == "GET":
        if('userinfo' in session):
            session.pop('userinfo', None)  # remove userinfo from session


        return render_template("register_page.html")
    elif request.method == "POST":
        print("post mu")
        if ('userinfo' in session):
            print("userinfo session'da var mı")
            userinfo = session['userinfo']
            session.pop('userinfo', None) # remove userinfo from session
            print("userinfo session'dan cıktı mı")
            print(session)
            command = """INSERT INTO PASSENGERS (country_id, passenger_name, passenger_last_name, email, gender, passport_id)
                         VALUES (%(country_id)s,
                                 '%(passenger_name)s',
                                 '%(passenger_last_name)s',
                                 '%(email)s',
                                 '%(gender)s',
                                 %(passport_id)s);"""
            execute_sql(command % {'country_id': request.form['country_id'], 'passenger_name': request.form['passenger_name'], 'passenger_last_name': request.form['passenger_last_name'],'email': request.form['email'], 'gender': request.form['gender'], 'passport_id': userinfo[2]}) # add to table PASSENGERS
            print("ilk execute")
            command = """ INSERT INTO USERS (username, password, passport_id) VALUES ('%(username)s', '%(password)s', %(passport_id)s);"""
            execute_sql(command % {'username': userinfo[0], 'password': userinfo[1], 'passport_id': userinfo[2]}) # add to table USERS
            print("return oncesi burası")
            return redirect(url_for("home_page"))
            
        username = request.form["username"]
        command = """ select username from USERS where username = '%(username)s'"""
        result = execute_sql(command % {'username': username})
        if (result != -2): # -2 means return of the select call is empty
            flash("Username already in use.")
            return redirect(url_for("register_page"))
        else:
            hash_pwd = hasher.hash(request.form["password"])
            passport_id = request.form["passport_id"]
            command = """ select passport_id from PASSENGERS where passport_id = %(passport_id)s"""
            result = execute_sql(command % {'passport_id': passport_id})
            if (result != -2): # -2 means return of the select call is empty
                command = """ INSERT INTO USERS (username, password, passport_id) VALUES ('%(username)s', '%(password)s', %(passport_id)s);"""
                result = execute_sql(command % {'username': username, 'password': hash_pwd, 'passport_id': passport_id})
                flash("User found in database.  Register completed.")
                return redirect(url_for("home_page"))
            else:
                flash("User not found in database.")
                session['userinfo'] = (username, hash_pwd, passport_id)
                print(session)
                return render_template("register_page_2.html", username = username, passport_id = passport_id) #html page not made

def user_page():
    if request.method == "GET":
        return render_template("user_page.html")   

def ticket_search_page():
    if request.method == "GET":
        return render_template("ticket_search_page.html")    
    elif request.method == "POST":
        try: #get all forms and check if they are empty or not
            min_date = request.form["min_date"]
            max_date = request.form["max_date"]
            origin = request.form["origin"]
            destination = request.form["destination"]
        except:
            flash("Please fill all forms")
            return render_template("flight_search_page")
        # write sql query to select country id based on for input
        command = """SELECT flight_id, departure_date, arrival_date, duration FROM FLIGHTS 
                    WHERE depature_date >= '%(min_date)s' AND arrival_date <= '%(max_date)s' """ # if possible also select departure and arrival airports
        data = execute_sql(command % {'min_date': min_date, 'max_date': max_date})
        session['ticket_search'] = data
        return url_for("ticket_view_page")

def ticket_view_page():
    if request.method == "GET":
        return render_template("ticket_search_page.html", data = session['ticket_search'])
        session.pop('ticket_search', None)  
    elif request.method == "POST":
        flight_id = request.form("flight_id")
        return url_for("ticket_buy_page", flight_id = flight_id) #send url parameter

def ticket_buy_page(): # displays captain name, captain photo (when blob is complete), origin airline, destination airline, departure airline, flight duration
    if request.method == "GET":
        flight_id = request.args.get('flight_id')
        #command selects relevant flight info
        command = """SELECT """
        return render_template("ticket_buy_page.html", ) 
    elif request.method == "POST": #buy ticket
        user = current_user.name
        if (user == 'admin'):
            flash("admins cannot buy tickets")
            return url_for('home_page')
        else:
            command = """SELECT * FROM USERS INNER JOIN PASSENGERS ON (USERS.passport_id = PASSENGERS.passenger_id)
                         WHERE USERS.username = '%(username)s'"""
            passenger_data = (execute_sql(command % {'username': current_user.name}))
        command = """ """
        execute_sql(command)
        flash("Ticket purchased")
        return url_for("home_page")
        
    




