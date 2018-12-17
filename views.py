import os
import random
from passlib.hash import pbkdf2_sha256 as hasher
import psycopg2 as dbapi2
import datetime
from flask import abort, current_app, render_template, flash
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_required, current_user, login_user, logout_user
from psycopg2.tests import dsn
import string
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
    today = datetime.datetime.today()
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
            passport_id = request.form['passport_id']
            passenger_name = request.form['passenger_name']
            passenger_last_name = request.form['passenger_last_name']

            gender = request.form['gender']
            if (country_id == '' or passport_id == '' or passenger_name == '' or passenger_last_name == '' or gender == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender)
                         VALUES (%(country_id)s,
                                 %(passport_id)s,
                                 '%(passenger_name)s',
                                 '%(passenger_last_name)s',
                                 '%(gender)s');"""



            data = execute_sql(command % {'country_id': country_id, 'passport_id': passport_id, 'passenger_name': passenger_name, 'passenger_last_name': passenger_last_name, 'gender': gender})
            print(data)
            if (data == -1):
                flash("Something went wrong. Please try again.")

        elif (my_table == 'FLIGHTS'):
            route_id = request.form['route_id']
            departure_date = str(request.form['departure_date'])
            arrival_date = departure_date
            departure_date += ' 10:00:00'
            print(departure_date)
            fuel_liter = request.form['fuel_liter']
            time_hours = int(request.form['time_hours'])
            gate_number = int(request.form['gate_number'])
            arrival_date = arrival_date + ' ' + str(10+time_hours) + ':00:00'
            print(arrival_date)

            if (route_id == ''  or departure_date == '' or arrival_date == '' or fuel_liter == '' or time_hours == '' or gate_number == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))

            command = "select aircraft_id from aircrafts where airline_id = (select airline_id from route_airline where route_id = %(route_id)s);"
            data = execute_sql(command % {'route_id': route_id})
            print(data)
            num = random.randint(1,7)
            try:
                aircraft_id = data[num][0]
            except:
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours, gate_number)
                         VALUES (%(route_id)s,
                                 %(aircraft_id)s,
                                 timestamp '%(departure_date)s',
                                 timestamp '%(arrival_date)s',
                                 %(fuel_liter)s,
                                 %(time_hours)s,
                                 %(gate_number)s);"""


            data = execute_sql(command % {'route_id': route_id, 'aircraft_id': aircraft_id, 'departure_date': departure_date, 'arrival_date': arrival_date, 'fuel_liter': fuel_liter, 'time_hours': time_hours, 'gate_number': gate_number})
            print(data)
            if(data == -1):
                flash("Something went wrong. Please try again.")


        elif (my_table == 'BOOKINGS'):
            flight_id = request.form['flight_id']

            passenger_id = request.form['passenger_id']
            purchase_time = str(datetime.datetime.now())[:19]
            class_of_seat = request.form["class_of_seat"]
            payment_type = request.form["payment_type"]
            seat = str(random.randint(1, 99)) + random.choice('ABCD')
            fare = request.form["fare"]


            if (flight_id == '' or passenger_id == '' or payment_type == '' or class_of_seat == '' or fare == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO BOOKINGS (flight_id, passenger_id, payment_type, purchase_time, seat, class_of_seat, fare)
                                             VALUES (%(flight_id)s,
                                                     %(passenger_id)s,
                                                     '%(payment_type)s',
                                                    TIMESTAMP '%(purchase_time)s',
                                                    '%(seat)s',
                                                    '%(class_of_seat)s',
                                                    %(fare)s);"""
            data = execute_sql(
                command % {'flight_id': flight_id, 'passenger_id': passenger_id, 'payment_type': payment_type,
                           'purchase_time': purchase_time, 'seat': seat, 'class_of_seat': class_of_seat, 'fare': fare})
            if(data == -1):
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))

            command = "UPDATE FLIGHTS SET number_passengers = number_passengers + 1 WHERE flight_id = %(flight_id)s;"
            data = execute_sql(command % {'flight_id': flight_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))


        elif (my_table == 'AIRCRAFTS'):
            airline_id = request.form['airline_id']

            capacity = request.form['capacity']

            company_name = request.form['company_name']

            model_name = request.form['model_name']
            maximum_range_km = request.form['maximum_range_km']

            year_produced = request.form['year_produced']

            if (airline_id == '' or capacity == '' or company_name == '' or model_name == '' or maximum_range_km == '' or year_produced == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced)
                         VALUES (%(airline_id)s,
                                 %(capacity)s,
                                 '%(company_name)s',
                                 '%(model_name)s',
                                 %(maximum_range_km)s,
                                 %(year_produced)s);"""


            data = execute_sql(command % { 'airline_id': airline_id, 'capacity': capacity, 'company_name': company_name, 'model_name': model_name, 'maximum_range_km': maximum_range_km, 'year_produced': year_produced})
            print(data)
            if (data == -1):
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))

        elif (my_table == 'ROUTES'):
            dep_airport_id = request.form['dep_airport_id']

            arr_airport_id = request.form['arr_airport_id']

            route_name = request.form['route_name']

            distance_km = request.form['distance_km']
            number_of_airlines = request.form['number_of_airlines']
            intercontinental = request.form['intercontinental']

            active_since = request.form['active_since']

            altitude_feet = request.form['altitude_feet']


            if (dep_airport_id == '' or arr_airport_id == '' or route_name == '' or distance_km == '' or number_of_airlines == '' or intercontinental == '' or active_since == '' or altitude_feet == '' ):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet)
                         VALUES (%(dep_airport_id)s,
                                 %(arr_airport_id)s,
                                 '%(route_name)s',
                                 %(distance_km)s,
                                 %(number_of_airlines)s,
                                 '%(intercontinental)s',
                                 %(active_since)s,
                                 %(altitude_feet)s);"""


            data = execute_sql(command % { 'dep_airport_id': dep_airport_id, 'arr_airport_id': arr_airport_id, 'route_name': route_name, 'distance_km': distance_km, 'number_of_airlines': number_of_airlines, 'intercontinental': intercontinental, 'active_since': active_since, 'altitude_feet': altitude_feet})
            print(data)
            if (data == -1):
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))

        elif (my_table == 'STAFF'):
            country_id = request.form['country_id']

            airline_id = request.form['airline_id']

            job_title = request.form['job_title']

            staff_name = request.form['staff_name']
            staff_last_name = request.form['staff_last_name']

            start_date = request.form['start_date']

            gender = request.form['gender']

            if (country_id == '' or airline_id == '' or job_title == '' or staff_name == '' or staff_last_name == '' or start_date == '' or gender == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_add_page"))
            # rewrite command so that empty forms do not change during the update command
            command = """INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender)
                         VALUES (%(country_id)s,
                                 %(airline_id)s,
                                 '%(job_title)s',
                                 '%(staff_name)s',
                                 '%(staff_last_name)s',
                                 date '%(start_date)s',
                                 '%(gender)s');"""


            data = execute_sql(command % { 'country_id': country_id, 'airline_id': airline_id, 'job_title': job_title, 'staff_name': staff_name, 'staff_last_name': staff_last_name, 'start_date': start_date, 'gender': gender})
            print(data)
            if (data == -1):
                flash("Something went wrong. Please try again.")

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
            if (data == -1):
                flash("Something went wrong. Please try again.")
            else:
                flash("Entry deleted successfully.")


        elif (my_table == 'FLIGHTS'):
            flight_id = request.form['flight_id']

            if (flight_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM FLIGHTS 
                             WHERE flight_id = %(name)s;"""

            data = execute_sql(command % {'name': flight_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
            else:
                flash("Entry deleted successfully.")

        elif (my_table == 'BOOKINGS'):
            flight_id = request.form['flight_id']
            passenger_id = request.form['passenger_id']

            if (flight_id == '' or passenger_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            command = """SELECT * FROM BOOKINGS 
                                                     WHERE (flight_id = %(flight_id)s) and (passenger_id = %(passenger_id)s);"""
            data = execute_sql(command % {'flight_id': flight_id, 'passenger_id': passenger_id})
            if (data == -2):
                flash("There is no such booking")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM BOOKINGS 
                             WHERE (flight_id = %(flight_id)s) and (passenger_id = %(passenger_id)s);"""

            data = execute_sql(command % {'flight_id': flight_id, 'passenger_id': passenger_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
            else:
                flash("Entry deleted successfully.")
                command = "UPDATE FLIGHTS SET number_passengers = number_passengers - 1 WHERE flight_id = %(flight_id)s;"
                data = execute_sql(command % {'flight_id': flight_id})
                if (data == -1):
                    flash("Something went wrong. Please try again.")
                    return redirect(url_for("admin_page"))


        elif (my_table == 'AIRCRAFTS'):
            aircraft_id = request.form['aircraft_id']

            if (aircraft_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM AIRCRAFTS 
                             WHERE aircraft_id = %(name)s;"""

            data = execute_sql(command % {'name': aircraft_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
            else:
                flash("Entry deleted successfully.")


        elif (my_table == 'ROUTES'):
            route_id = request.form['route_id']

            if (route_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM ROUTES 
                             WHERE route_id = %(name)s;"""

            data = execute_sql(command % {'name': route_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
            else:
                flash("Entry deleted successfully.")


        elif (my_table == 'STAFF'):
            staff_id = request.form['staff_id']

            if (staff_id == ''):
                flash("Insufficient Entry")
                return redirect(url_for("admin_delete_page"))
            # rewrite command so that FLIGHTS forms do not change during the update command
            command = """DELETE FROM FLIGHTS 
                                                     WHERE flight_id = (SELECT flight_id from STAFF_FLIGHT WHERE staff_id = %(name)s);"""

            data = execute_sql(command % {'name': staff_id})
            if (data == -1):
                flash("Something went wrong. Please try again.")
                return redirect(url_for("admin_page"))
            else:
                command = """DELETE FROM STAFF 
                                 WHERE staff_id = %(name)s;"""

                data = execute_sql(command % {'name': staff_id})

                if (data == -1):
                    flash("Something went wrong. Please try again.")
                else:
                    flash("Entry deleted successfully.")

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
            try:
                pic = request.files["file_data"]
                file_data = pic.read().decode("base64")
                print("data:")
                print(file_data)
                #image_command = """UPDATE PASSENGERS SET """
                
            except:
                file_data = None
            try:
                gender = request.form["gender"] #check if radio is selected or not
            except: #radio left empty
                gender = ""
            values = [request.form['passenger_id'], request.form["email"], request.form["country_id"], request.form["name"], request.form["middlename"],               request.form["surname"], request.form["passport_id"] , gender]
            column_names = ["passenger_id", "email", "country_id", "passenger_name", "passenger_middle_name", "passenger_last_name", "passport_id" , "gender"]
        elif (my_table == 'STAFF'):
            table_name = "STAFF"
            try:
                print("blob debug0")
                pic = request.files["file_data"]
                print("blob debug1")
                file_data = pic.read()
                print("blob debug2")
                file_data = file_data.encode("base64")
                print("data:")
                print(file_data)
            except:
                print("blob debug3")
                file_data = ""
            try:
                gender = request.form["gender"] #check if radio is selected or not
            except: #radio left empty
                gender = ""
                
            values = [request.form["staff_id"], request.form["country_id"], request.form["airline_id"], request.form["job_title"], request.form["name"], request.form["surname"], request.form["start_date"], gender, file_data] 
            column_names = ["staff_id", "country_id", "airline_id", "job_title", "staff_name", "staff_last_name", "start_date", "gender", "file_data" ]
        elif (my_table == 'BOOKINGS'):
            table_name = "BOOKINGS"
            primary_key_count = 2
            values = [request.form["booking_id"], request.form["flight_id"], request.form["passenger_id"], request.form["payment_type"],request.form["seat_number"], request.form["class_type"], request.form["fare"]]
            column_names = ["booking_id", "flight_id", "passenger_id", "payment_type", "seat_number", "class_type", "fare"]
        elif (my_table == 'FLIGHTS'):
            table_name = "FLIGHTS"
            values = [request.form["flight_id"], request.form["aircraft_id"], request.form["route_id"], request.form["departure_date"], request.form["arrival_date"], request.form["fuel_liter"], request.form["time_hours"], request.form["average_altitude"], request.form["gate_number"]]
            column_names = ["flight_id", "aircraft_id", "route_id", "departure_date", "arrival_date", "fuel_liter", "time_hours", "averge altitude", "gate_number"]
        elif (my_table == 'AIRCRAFTS'):
            table_name = "AIRCRAFTS"  
            values = [request.form["aircraft_id"], request.form["airline_id"],request.form["capacity"], request.form["company_name"],request.form["model_name"], request.form["maximum_range"], request.form["year_produced"]]
            column_names =  ["aircraft_id", "airline_id","capacity", "company_name", "model_name", "maximum_range_km", "year_produced"]
        elif (my_table == 'ROUTES'):
            table_name = "ROUTES"  
            values = [request.form["route_id"], request.form["dep_airport_id"], request.form["arr_airport_id"], request.form["route_name"], request.form["distance_km"], request.form["number_of_airlines"], request.form["altitude_feet"], request.form["intercontinental"],request.form["active_since"]]
            column_names = ["route_id", "dep_airport_id", "arr_airport_id", "route_name", "distance_km", "number_of_airlines", "altitude_feet","intercontinental", "active_since"]  

        command = sqlgen_update(table_name, column_names, values, primary_key_count)
        data = execute_sql(command)
        if (data == -1):
            flash("Something went wrong. Please try again.")
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
        if(data == -2):
            flash("Nothing to show. No records found.")
            return redirect(url_for("admin_page"))
        data[1:] = sorted(data[1:])
        return render_template("admin_view_page.html", table=my_table, data=data)

@login_required
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

@login_required
def ticket_search_page():
    if request.method == "GET":
        return render_template("ticket_search_page.html")    
    elif request.method == "POST":
         #get all forms and check if they are empty or not
         min_date = request.form["min_date"]
         print(min_date)
         max_date = request.form["max_date"]
         print(max_date)
         dep_country_name = request.form["dep_country_name"]
         print(dep_country_name)
         arr_country_name = request.form["arr_country_name"]
         print(dep_country_name)


         if(min_date == "" or max_date == "" or dep_country_name == "" or arr_country_name == ""):
              flash("Please give me enough information.")
              return redirect(url_for("ticket_search_page"))
         else:
              # write sql query to select valid flights based on form inputs
              command = """SELECT flight_id, departure_date, arrival_date, time_hours, route_name from FLIGHTS INNER JOIN ROUTES ON FLIGHTS.route_id = ROUTES.route_id INNER JOIN 
              AIRPORTS ON ROUTES.dep_airport_id = AIRPORTS.airport_id WHERE 
              departure_date <= '%(max_date)s' AND departure_date >= '%(min_date)s' AND AIRPORTS.country_id = (SELECT country_id FROM COUNTRIES WHERE country_name = '%(dep_country_name)s') 
              INTERSECT 
              SELECT flight_id, departure_date, arrival_date, time_hours, route_name from FLIGHTS INNER JOIN ROUTES ON FLIGHTS.route_id = ROUTES.route_id INNER JOIN 
              AIRPORTS ON ROUTES.arr_airport_id = AIRPORTS.airport_id WHERE 
              departure_date <= '%(max_date)s' AND departure_date >= '%(min_date)s' AND AIRPORTS.country_id = (SELECT country_id FROM COUNTRIES WHERE country_name = '%(arr_country_name)s');"""

              data = execute_sql(command % {'min_date': min_date, 'max_date': max_date, 'dep_country_name': dep_country_name, 'arr_country_name': arr_country_name})
              if(data == -2):
                   flash("No flights found. Please try again.")
                   return redirect(url_for("ticket_search_page"))
              else:
                   print(data)
                   ids = [r[0] for r in data]
                   ids = ids[1:]
                   session['ticket_search'] = data
                   session['id_values'] = ids
                   return redirect(url_for("ticket_view_page"))

    flash("Something went wrong.")
    return redirect(url_for("home_page"))

@login_required
def ticket_view_page():
    if request.method == "GET":
        data = session['ticket_search']
        ids = session['id_values']
        session.pop('ticket_search', None)
        session.pop('ticket_buy_info', None)
        session.pop('id_values', None)
        return render_template("ticket_view_page.html", data = data, ids = ids )

    elif request.method == "POST":
        flight_id = request.form["id"]
        
        session['ticket_buy_flight_id'] = flight_id
        try:
            show_info = request.form["show_info"]      
            session['ticket_buy_info'] = show_info
        except:
            session['ticket_buy_info'] = False
            
        return redirect(url_for("ticket_buy_page")) #send url parameter
@login_required
def ticket_buy_page(): # displays captain name, captain photo (when blob is complete), origin airline, destination airline, departure airline, flight duration
    if request.method == "GET":
        flight_id = session['ticket_buy_flight_id']
        show_info = session['ticket_buy_info']
        #command selects relevant flight info
        command = """SELECT flight_id, departure_date, arrival_date, time_hours, route_name, staff_name, staff_last_name, job_title FROM ROUTES, FLIGHTS, STAFF 
                            where flight_id = %(flight_id)s and 
                            staff_id = (SELECT staff_id FROM STAFF_FLIGHT WHERE flight_id = %(flight_id)s) and
                            routes.route_id = (SELECT route_id FROM FLIGHTS WHERE flight_id = %(flight_id)s);"""
        data = execute_sql(command % {'flight_id': flight_id})
        command = """SELECT file_data FROM ROUTES, FLIGHTS, STAFF 
                            where flight_id = %(flight_id)s and 
                            staff_id = (SELECT staff_id FROM STAFF_FLIGHT WHERE flight_id = %(flight_id)s) and
                            routes.route_id = (SELECT route_id FROM FLIGHTS WHERE flight_id = %(flight_id)s);"""
        file_data = execute_sql(command % {'flight_id': flight_id}) #store image binary data    
        #print("----------------------------------------------------------------------")        
        #print(file_data)
        if(show_info):
            return render_template("ticket_buy_page.html", data=data, picture = file_data[1][0])
        else:
            return render_template("ticket_buy_page_noinfo.html", data=data)
    elif request.method == "POST": #buy ticket
        username = current_user.username
        if (username == 'admin'):
            flash("admins cannot buy tickets")
            return url_for('home_page')
        else:
            print(username)
            flight_id = session['ticket_buy_flight_id']
            class_of_seat = request.form["class_type"]
            payment_type = request.form["payment_type"]
            command = """SELECT passenger_id FROM USERS INNER JOIN PASSENGERS ON (USERS.passport_id = PASSENGERS.passport_id)
                         WHERE username = '%(username)s'"""
            data = (execute_sql(command % {'username': username}))
            passenger_id = data[1][0]
            purchase_time = str(datetime.datetime.now())[:19]
            seat = str(random.randint(1,99)) + random.choice('ABCD')
            fare = 100 if(class_of_seat == 'Budget')  else 200 if (class_of_seat == 'Economy') else 300 if (class_of_seat == 'Business') else 400

        command = """INSERT INTO BOOKINGS (flight_id, passenger_id, payment_type, purchase_time, seat, class_of_seat, fare)
                                 VALUES (%(flight_id)s,
                                         %(passenger_id)s,
                                         '%(payment_type)s',
                                        TIMESTAMP '%(purchase_time)s',
                                        '%(seat)s',
                                        '%(class_of_seat)s',
                                        %(fare)s);"""
        data = execute_sql(command % {'flight_id': flight_id, 'passenger_id': passenger_id, 'payment_type': payment_type, 'purchase_time': purchase_time, 'seat': seat, 'class_of_seat': class_of_seat, 'fare': fare})
        command = "UPDATE FLIGHTS SET number_passengers = number_passengers + 1 WHERE flight_id = %(flight_id)s;"
        data = execute_sql(command % {'flight_id': flight_id})

        flash("Ticket purchased")
        return redirect(url_for("user_page"))

    flash("Something went wrong.")
    return redirect(url_for("home_page"))




@login_required
def user_flights_page():
    username = current_user.username
    if (username == 'admin'):
        flash("admins cannot buy tickets")
        return url_for('home_page')
    elif (username == ''):
        flash("You must login to buy tickets")
        return url_for('home_page')
    else:
        if request.method == "GET":

            command = """SELECT passenger_id FROM USERS INNER JOIN PASSENGERS ON (USERS.passport_id = PASSENGERS.passport_id)
                                     WHERE username = '%(username)s'"""
            data = (execute_sql(command % {'username': username}))
            passenger_id = data[1][0]
            command = """SELECT FLIGHTS.flight_id, passenger_name, passenger_last_name, route_name, departure_date, arrival_date, seat, class_of_seat, gate_number FROM ROUTES, FLIGHTS, BOOKINGS, PASSENGERS WHERE
                                BOOKINGS.passenger_id = %(passenger_id)s and 
                                bookings.flight_id = flights.flight_id and 
                                flights.route_id = routes.route_id and 
                                passengers.passenger_id = bookings.passenger_id;"""
            data = execute_sql(command % {'passenger_id': passenger_id})
            print(data)
            if(data == -2):
                data = [[]]
            else:

                return render_template("user_flights_page.html", data=data)
            flash("You have no tickets purchased.")
            return redirect(url_for("user_page"))

        flash("Something went wrong.")
        return redirect(url_for("home_page"))


