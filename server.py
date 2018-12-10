from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import session
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
    app.secret_key = 'Q8z/n/xec]/b"_5#y2L"F4' #secret key needed for cookies
    
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)


    # app.add_url_rule("/add-passenger", view_func=views.passenger_add_page, methods=["GET", "POST"])
    
    
    app.add_url_rule("/admin_page", view_func=views.admin_page)
    app.add_url_rule("/admin_page/select_table", view_func=views.admin_select_table, methods=["GET", "POST"])
    
    app.add_url_rule("/admin_page/add", view_func=views.admin_add_page, methods=["GET", "POST"]) 
    app.add_url_rule("/admin_page/delete", view_func=views.admin_delete_page, methods=["GET", "POST"])
    app.add_url_rule("/admin_page/update", view_func=views.admin_update_page, methods=["GET", "POST"])
    app.add_url_rule("/admin_page/view", view_func=views.admin_view_page, methods=["GET", "POST"])
    #app.add_url_rule("/admin_page/sql", view_func=views.admin_sql_page, methods=["GET", "POST"])
    
    lm.init_app(app)
    lm.login_view = "login_page"



    return app


app = create_app()


if __name__ == "__main__":
    port = app.config.get("PORT", 5001)
    app.run()
