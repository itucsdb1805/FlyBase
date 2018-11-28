from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask_login import LoginManager
from user import get_user

import views
from flight import Flight

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)

    app.add_url_rule(
        "/add_country", view_func=views.add_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/countries", view_func=views.countries_page)
    # app.add_url_rule("/add-passenger", view_func=views.passenger_add_page, methods=["GET", "POST"])

    lm.init_app(app)
    lm.login_view = "login_page"



    return app


app = create_app()


if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run()
