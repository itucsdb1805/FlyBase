from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2


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


def get_user(username):
    getPassword = """SELECT (password) FROM USERS WHERE username = '%(name)s'"""
    password = execute_sql(getPassword % {'name': username})[1][0]
    #password = current_app.config["PASSWORDS"].get(username)
    user = User(username, password) if password else None
    if user is not None:
        user.is_admin = True if (username == 'admin') else False
    return user
