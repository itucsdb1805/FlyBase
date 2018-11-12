from flask import Flask

import views
from database import Database
from flight import Flight


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/flights", view_func=views.flights_page)
    app.add_url_rule("/flights/<int:flight_key>", view_func=views.flight_page)

    db = Database()
    db.add_flight(Flight("IST-ESB", date="10-10-2018", airport="IST"))
    db.add_flight(Flight("IST-LON", date="09-10-2018", airport="IST"))
    app.config["db"] = db

    return app


app = create_app()


if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)