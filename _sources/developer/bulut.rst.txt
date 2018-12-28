Parts Implemented by Kadir Bulut Ozler
================================

Functions in user.py
------------




execute_sql()
^^^^^^^^
.. code-block:: python
  def execute_sql(command):
      print("executing...")
      print(command)
      #command = """UPDATE COUNTRIES SET country_name = Turkey WHERE country_id = 1;"""
      try:
              url = os.getenv("DATABASE_URL")  #url = "postgres://itucs:itucspw@localhost:32769/itucsdb"#
              print("debug0")
              connection = dbapi2.connect(url)
              print("debug1")
              cursor = connection.cursor()
              print("debug2")
              cursor.execute(command)
              print("Execute works!!")

              connection.commit()

      except dbapi2.DatabaseError:
              print("dataerror2")
              print(dbapi2.DatabaseError)
              connection.rollback()
              return -1;

      try:
              data_column = []
              data_content = cursor.fetchall()
              print(data_content)
              if (data_content == [] or data_content == [[]]):
                 print("data bos")
                 return -2
              data_column.append(tuple([desc[0] for desc in cursor.description]))
              data_column += data_content
              cursor.close()
              connection.close()

      except dbapi2.DatabaseError:
              print("dataerror3")
              print(dbapi2.DatabaseError)
              connection.rollback()
              return -3

  return data_column
  
  
  
This function takes a string which contains PostgreSQL code and executes it.  The first try, except loop (implemented by member Ahmed) tries to connect to the sql server.  If successful it executes the sql code and if there is any query result from this code it saves it the variable “data” then moves on to the seconds try, except loop.  If unsuccessful it returns -1.  The second try, except loop (implemented  by member Bulut) checks if the variable “data” is empty.  If it is then the value -2 is returned.  If “data” is not empty, the names of the columns are appended to the list (data) as the first item and data is returned.



User()
^^^^^^^^
.. code-block:: python
  class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.is_admin = False

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active
  
This class stores user information and has some getter methods.



get_user()
^^^^^^^^
.. code-block:: python
  def get_user(username):
    getPassword = """SELECT (password) FROM USERS WHERE username = '%(name)s'"""
    password = execute_sql(getPassword % {'name': username})
    if(password != -2):
        password = password[1][0]
        user = User(username, password) if password else None
    else:
        user = None
    #password = current_app.config["PASSWORDS"].get(username)

    if user is not None:
        user.is_admin = True if (username == 'admin') else False
    return user
  
  
  
This function return user information as the object “user” as the class “User”. This function gets a username as a string input.  The input is used to make an sql query.  The query is executed with the function execute_sql() and the password is taken from the result.  If the password is not found, then the user does not exist and the return value is None.  Then the user is checked if it is an admin.  Then with this information an object of the class User is constructed and returned.


Functions in views.py
------------

login_page()
^^^^^^^^
.. code-block:: python
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



This function allows the user to log in. If username exists, it checks if the password is correct by hashing it and comparing with the hashed version of the password that belongs to given username. It flashes necessary message if user successfully log in or not.

logout_page()
^^^^^^^^
.. code-block:: python
def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


This function is used to logout by calling the function logout_user() and then render the home page.


home_page()
^^^^^^^^
.. code-block:: python
def home_page():
    today = datetime.datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


This function is used to render the home page.  It gets the current day and sends it as the variable “day” to home.html when rendering.


admin_page()
^^^^^^^^
.. code-block:: python
@login_required
def admin_page():
    if not current_user.is_admin:
        abort(401)
    return render_template("admin_page.html")


This is used to display the admin page.  It checks if the user is an admin and acts accordingly.


admin_add_page()
^^^^^^^^
.. code-block:: python
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


This function is used to add rows to a table.  This function first checks if the user is an admin.  If not then the function aborts.  The function gets the table name from the session ‘table’ then stores it as the variable my_table.  If there session is empty the function aborts. If the function is called using ‘GET’ then the html page “admin_add_page.html” is rendered with the parameter as the variable table so that the correct form is displayed in the html page.  After submitting the form the function will be called using ‘POST’.  Here the function checks the table name using if and elif.  Then depending on the table the proper request forms are called and the correct sql add code is generated and executed using the function execute_sql().  Then the page for admin page is called. Each user implemented the parts for their tables.




admin_delete_page()
^^^^^^^^
.. code-block:: python
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



This function is used to delete rows from a table using the primary key(s).  This function first checks if the user is an admin.  If not then the function aborts.  The function gets the table name from the session ‘table’ then stores it as the variable my_table.  If there session is empty the function aborts. If the function is called using ‘GET’ then the html page “admin_delete_page.html” is rendered with the parameter as the variable table so that the correct form is displayed in the html page.  After submitting the form the function will be called using ‘POST’.  Here the function checks the table name using if and elif.  Then depending on the table the proper request forms are called and the correct sql delete code is generated and executed using the function execute_sql().  Then the page for admin page is called.  Each user implemented the parts for their tables.



admin_update_page()
^^^^^^^^
.. code-block:: python
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
            values = [request.form["flight_id"], request.form["passenger_id"], request.form["payment_type"],request.form["seat_number"], request.form["class_type"], request.form["fare"]]
            column_names = [ "flight_id", "passenger_id", "payment_type", "seat_number", "class_type", "fare"]
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


This function is used to update rows in a table using the primary key(s).  This function first checks if the user is an admin.  If not then the function aborts.  The function gets the table name from the session ‘table’ then stores it as the variable my_table.  If there session is empty the function aborts. If the function is called using ‘GET’ then the html page “admin_update_page.html” is rendered with the parameter as the variable table so that the correct form is displayed in the html page.  After submitting the form the function will be called using ‘POST’.  Here the function sets the variables table_name, values, column_keys and primary_key_count are set according to the table name.  Then the sql code is generated using these variables and the function sqlgen_update().  This code is then executed using the function execute_sql().  Depending on the result of execute_sql() an error message is displayed and the page for admin_page is called. Each user implemented the parts for their tables.




admin_view_page()
^^^^^^^^
.. code-block:: python
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

This function is used to show all columns and rows in a table.  This function first checks if the user is an admin.  If not then the function aborts.  The function gets the table name from the session ‘table’ then stores it as the variable my_table.  If there session is empty the function aborts. The variable my_table is used to generate and execute an sql query using execute_sql() and the query result is saved as the variable ‘data’.  If the variable ‘data’ is empty (set as -2) then an error message is flashed on screen.  Else the data is sorted and the html page “admin_view_page.html” is called with the parameters ;data’ and my_table. Each user implemented the parts for their tables.



register_page()
^^^^^^^^
.. code-block:: python
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

This function is used to make registrations.  If the function is called with the method “GET” then the session ‘userinfo’ is cleared and the html page “register_page.html” is rendered.  In this html page there is a form for username, password and passport id.  Once the form is submitted the function is called with the method “POST”.  Here we check if the session ‘userinfo’ exists.  If it does not exist then we check if the username exists by executing a query for the table USERS using execute_sql().  If the username exists then an error message is flashed and the register page is rendered again.  If the username does not exist then the password and passport id are requested from the forms and the password is hashed using hasher.hash().  Then we make and execute a query in order to check if the passport id already exists in the table PASSENGERS.  If it does exist then the information from this table is used to complete the registration.  If it does not exist then the html page then we make a session called ‘userinfo’ and store the username, hashed password and passport id here.  Then “register_page_2” is rendered with the parameters username and passport_id.  Here there are more forms that must be filled.  After submitting this form the function is called using the method “POST”.  This time the function checks that a session called ‘userinfo’ exists and enters another part of the code.  Here the forms from register_page_2.html are requested.  Using these values and the values from session ‘userinfo’ an sql insertion command is generated to insert the relevant information to the table PASSENGERS and the table USERS.  Then the page for home_page is called.
For more information view the registration operation is user documents.
(Members Ahmed and Bulut implemented this part together with equal amount of work done)




user_page()
^^^^^^^^
.. code-block:: python
def user_page():
    if request.method == "GET":
        return render_template("user_page.html")   

Here the html page “user_page.html” is rendered.  This page is for selecting the operation for buying tickets or viewing the users purchased flights.


ticket_search_page()
^^^^^^^^
.. code-block:: python
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

This function is used to search for flights meeting a certain criteria which is given by the user.  If the function is called using the method “GET” then the html page “ticket_search_page.html” is rendered.  Here there are forms which ask user for the departure and arrival country and the min and max date for the flights the user wants.  Once these are submitted this function is called with the method “POST”.  If the method is “POST” then the function request the forms and checks if the forms are empty.  If the forms are empty and error message is flashed and the html page is rendered again.  If the forms are valid then an sql code is set as the variable “command”.  This sql code find the departure_date, arrival_date, time_hours (flight time) and route_name columns for the criteria inputted by the user.  Or in other words it finds valid flights and information that meets the users criteria.  This code is executed using execute_sql() and the result is saved to the variable ‘data’.  If no results meeting the user criteria are found (data = -2) then an error message is flashed and ticket_search_page.html is rendered again.  If there are results then the variable data is stored in the session ‘ticket_search’ and the ids of the flights we found are stored in the session ‘id_values’.  Then the page ticket_view_page is called.
(Members Ahmed and Bulut implemented this part together with equal amount of work done)



ticket_view_page()
^^^^^^^^
.. code-block:: python
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

This page is used to view and select flight that have been searched by the user.  In this function if the method is “GET” then the function gets the information from the sessions ‘ticket_search’ and ‘id_values’ and stores them in the variables ‘data’ and ‘ids’ respectively.  Then pops the sessions: ‘ticket_search’, ‘ticket_buy_info’ and ‘id_values’.  Then the html page ‘ticket_view_page.html’ is rendered using with the parameters ‘ids’ and ‘data’.  This html page shows the flight ids and has a drop-down selection form for these flight ids.  This page also has a checkbox where the user can click to view detailed information about the flight they are selecting. After submitting this form this function is called with the method “POST”.  If the method is “POST” then the function request the forms and sets the sessions ‘ticket_buy_flight_id’ as the selected flight id and ‘ticket_buy_info’ as true or false depending on whether the checkbox in the form was selected or not.  Then the page for ticket_buy_page is called.
(Members Ahmed and Bulut implemented this part together with equal amount of work done)


ticket_buy_page()
^^^^^^^^
.. code-block:: python
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


This page is used to view information about a flight and purchase a ticket for this flight.  The sessions ‘ticket_buy_flight_id’ and ’ticket_buy_info’ is saved as the variables flight_id and show_info respectively.  Then a sql query that gets relevant flight info is executed using execute_sql() and saved to the variable ‘data’.  And another sql command that gets file_data (the image) from the table STAFF is executed and the result saved to the variable ‘file_data’, however since image uploading is not implemented this part is irrelevant.  Then depending on the variable show_info either the html page “ticket_buy_page.html” or “ticket_buy_page_noinfo.html” in rendered.  These pages contain some information about the flight and a form for purchasing a ticket.  After submitting the form then this function is called with the method “POST”.  If the method is “POST” then the function first gets the current users username and sets it as the variable ‘username’.  If the user is an admin then the purchase is not done and an error message is flashed.  If the user is not an admin, then the required forms are requested and an sql command that joins the tables USERS and PASSENGERS and finds the passenger_id of the current user using the username is executed using execute_sql().  The result is saved as the variable “data”.  The passenger_id is taken from the variable ‘data’ and saved as passenger_id, the variable purchase_time is set as the current time, the variable seat is randomly set and the fare is calculated using the variable class_of_seat, which was requested from the form.  Using these variables an sql insertion command is made to insert a row into the table BOOKINGS and executed using execute_sql().  Then the message “Ticket bought” is flashed on screen and the page for home page is called.
(Members Ahmed and Bulut implemented this part together with equal amount of work done)


user_flights_page()
^^^^^^^^
.. code-block:: python
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



This page shows the purchased flights for the current logged in user.  This function first checks if the user is an admin or is not logged in.  If these one of these checks passes then an error message is flashed and the page for home_page is called.  If the user is not an admin and is logged in, then the current user’s passenger id is found by executing an sql query using execute_sql().  The passenger id is stored to the variable passenger_id.  Then an sql query that gets relevant flight information from the table BOOKINGS is called and executed using execute_sql() and the result is saved to the variable “data”.  If “data” is -2, which means the user has no tickets purchased, than an error message is flashed and the page user_page is called.  If not then the html page “user_flights_page.html” is rendered with the parameter “data”.  This page shows all purchased flights.
