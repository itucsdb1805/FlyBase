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

from forms import LoginForm
from user import get_user


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)




@login_required
def add_page():
    if not current_user.is_admin:
        abort(401)

    statement = """INSERT INTO COUNTRIES (country_name)
        VALUES (%(name)s)"""


    if request.method == "GET":
        return render_template("add_country.html")
    else:
        form_name = request.form["name"]

        try:
            url =  os.getenv("DATABASE_URL")  #"postgres://itucs:itucspw@localhost:32769/itucsdb"
            connection = dbapi2.connect(url)
            cursor = connection.cursor()
            if (form_name):
                cursor.execute(statement, {'name': form_name})

                print("Execute works!")
                connection.commit()

            cursor.close()
            connection.close()
        except dbapi2.DatabaseError:
            print("dataerror1")
            print(dbapi2.DatabaseError)
            connection.rollback()
        finally:
            return redirect(url_for("countries_page"))

@login_required
def countries_page():

    statement = """SELECT country_id, country_name
        FROM COUNTRIES"""
    data = ""

    if request.method == "GET":
        return render_template("countries.html")

    try:

        url =  os.getenv("DATABASE_URL")  #"postgres://itucs:itucspw@localhost:32769/itucsdb"
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