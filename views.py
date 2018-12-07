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

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def execute_sql(command):
    print("executing...")
    print(command)
    #command = """UPDATE COUNTRIES SET country_name = Turkey WHERE country_id = 1;"""
    try:
            url = "postgres://itucs:itucspw@localhost:32770/itucsdb"#url = os.getenv("DATABASE_URL")  # 
            print("debug0")
            connection = dbapi2.connect(url)
            print("debug1")
            cursor = connection.cursor()
            print("debug2")
            cursor.execute(command)
            print("Execute works!")
            connection.commit()
            data = cursor.fetchall()
            cursor.close()
            connection.close()

    except dbapi2.DatabaseError:
            print("dataerror2")
            print(dbapi2.DatabaseError)
            connection.rollback()
            return -1;
    return data

@login_required
def add_page(): # rewrite using execute_sql()
    if not current_user.is_admin:
        abort(401)



    statement1 = """INSERT INTO COUNTRIES (country_name)
        VALUES (%(name)s)"""

    statement2 = """DELETE FROM COUNTRIES 
            WHERE country_name = %(name)s"""

    statement3 = """DELETE FROM COUNTRIES 
                """


    if request.method == "GET":
        return render_template("add_country.html")
    else:
        form_name = request.form['name']
        addOrDelete = request.form['addDeleteShow']
        print(addOrDelete)

        try:
            url = "postgres://itucs:itucspw@localhost:32770/itucsdb"#url = os.getenv("DATABASE_URL")  # 
            connection = dbapi2.connect(url)
            cursor = connection.cursor()
            if (addOrDelete == 'add'):
                if(form_name == ''):
                    flash("Country info cannot be empty.")
                    return redirect(url_for("add_page"))

                cursor.execute(statement1, {'name': form_name})
                print("add Execute works!")
                connection.commit()

            elif (addOrDelete == 'delete'):
                if (form_name == ''):
                    flash("Country info cannot be empty.")
                    return redirect(url_for("add_page"))


                cursor.execute(statement2, {'name': form_name})
                print("delete Execute works!")
                connection.commit()

            elif (addOrDelete == 'deleteAll'):
                cursor.execute(statement3)
                print("deleteAll Execute works!")
                connection.commit()


            elif (addOrDelete == 'show'):
                return redirect(url_for("countries_page"))

            cursor.close()
            connection.close()
            return redirect(url_for("countries_page"))

        except dbapi2.DatabaseError:
            print("dataerror1")
            print(dbapi2.DatabaseError)
            connection.rollback()


@login_required
def countries_page():  #rewrite using execute_sql()

    statement = """SELECT country_id, country_name
        FROM COUNTRIES"""
    data = ""

    if request.method == "GET":
        
        statement = """SELECT *
        FROM COUNTRIES"""
        data = ""
        url = "postgres://itucs:itucspw@localhost:32770/itucsdb" #os.getenv("DATABASE_URL")  #
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        cursor.execute(statement)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("countries.html", data=sorted(data))

    try:

        url = "postgres://itucs:itucspw@localhost:32770/itucsdb" #os.getenv("DATABASE_URL")
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        cursor.execute(statement)
        print("Execute works!")

        data = cursor.fetchall()
        print(data)
        for country_id, country_name in data:
            print('%(id)s: %(nm)s' % {'id': country_id, 'nm': country_name})
        cursor.close()
        connection.close()

    except dbapi2.DatabaseError:
        print("dataError2")
        connection.rollback()

    finally:
        return render_template("countries.html", data=sorted(data))
    
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
            return redirect(url_for("add_page"))  #change to admin_add_page
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
    return render_template("add_country.html")

@login_required
def admin_delete_page():
    if not current_user.is_admin:
        abort(401)
    return render_template("add_country.html")

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
        if (my_table == 'COUNTRIES'):
            new_name = request.form['country_name']
            new_id = request.form['country_id']
            #rewrite command so that empty forms do not change during the update command
            command = """UPDATE COUNTRIES 
                        SET country_name = '%(name)s'  
                        WHERE country_id = %(id)s;"""
            
            execute_sql(command % {'name': new_name, 'id' : new_id})
        return redirect(url_for("admin_page")) #change this into a page that displays whether operation was successful or not
        

