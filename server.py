from flask import Flask

import views
from database import Database
from movie import Movie


def create_app():
    appp = Flask(__name__)
    appp.config.from_object("settings")

    appp.add_url_rule("/", view_func=views.home_page)
    appp.add_url_rule("/movies", view_func=views.movies_page)
    appp.add_url_rule("/movies/<int:movie_key>", view_func=views.movie_page)


    db = Database()
    db.add_movie(Movie("Slaughterhouse-Five", year=1972))
    db.add_movie(Movie("The Shining"))
    appp.config["db"] = db

    return appp


if __name__ == "__main__":
    appp = create_app()
    port = appp.config.get("PORT", 5000)
    appp.run(host="0.0.0.0", port=port)
