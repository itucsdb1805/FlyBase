import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """ CREATE TABLE IF NOT EXISTS COUNTRIES(
            country_id serial PRIMARY KEY,
            country_name varchar(50) NOT NULL
            );""",

    """ CREATE TABLE IF NOT EXISTS AIRLINES(
            airline_id serial PRIMARY KEY,
            airline_name varchar(50) NOT NULL
            );""",

    " INSERT INTO AIRLINES(airline_name) VALUES ('Lufthansa'); ",
    " INSERT INTO AIRLINES(airline_name) VALUES ('Turk Hava Yollari'); ",
    " INSERT INTO AIRLINES(airline_name) VALUES ('Air France'); ",

    """ CREATE TABLE IF NOT EXISTS AIRCRAFTS(
            aircraft_id serial PRIMARY KEY,
            aircraft_name varchar(50) NOT NULL
            );""",

    " INSERT INTO AIRCRAFTS(aircraft_name) VALUES ('Boeing 747'); ",
    " INSERT INTO AIRCRAFTS(aircraft_name) VALUES ('Airbus A320'); ",
    " INSERT INTO AIRCRAFTS(aircraft_name) VALUES ('Boeing 767'); ",

    """ CREATE TABLE IF NOT EXISTS ROUTES(
            route_id serial PRIMARY KEY,
            route_name varchar(50) NOT NULL
            );""",

    " INSERT INTO ROUTES(route_name) VALUES ('ISTESB'); ",
    " INSERT INTO ROUTES(route_name) VALUES ('ISTLON'); ",
    " INSERT INTO ROUTES(route_name) VALUES ('LONCDG'); ",

    """ CREATE TABLE IF NOT EXISTS PASSENGERS(
            passenger_id serial PRIMARY KEY,
            name varchar (20) NOT NULL,
            middle_name varchar (20) DEFAULT NULL,
            surname varchar (20) NOT NULL,
            gender  varchar (1) NOT NULL
                CHECK (gender IN ( 'F' , 'M' ) ),
            birth_date date NOT NULL,
            country_id integer NOT NULL,
            flight_count integer DEFAULT 0,
            last_flight_day date DEFAULT NULL,
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            );""",

    """ CREATE TABLE IF NOT EXISTS AIRLINE_WORKERS(
            worker_id serial PRIMARY KEY,
            name varchar (20) NOT NULL,
            middle_name varchar (20) DEFAULT NULL,
            surname varchar (20) NOT NULL,
            gender  varchar (1) NOT NULL
                CHECK (gender IN ( 'F' , 'M' ) ),
            birth_date date NOT NULL,
            country_id integer NOT NULL ,
            flight_hours integer DEFAULT 0,
            airline_id integer NOT NULL REFERENCES AIRLINES(airline_ID) ON DELETE RESTRICT,
            job  varchar(15) NOT NULL
                CHECK (job IN ( 'pilot' , 'hostess' , 'other' ) ),
            photo varchar(50) DEFAULT './photos/default.jpg',
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            );""",

    """ CREATE TABLE IF NOT EXISTS FLIGHTS(
            flight_id serial PRIMARY KEY,
            airline_id integer NOT NULL REFERENCES AIRLINES(airline_id) ON DELETE RESTRICT,
            aircraft_id integer NOT NULL REFERENCES AIRCRAFTS(aircraft_id) ON DELETE RESTRICT,
            route_id integer NOT NULL REFERENCES ROUTES(route_id) ON DELETE RESTRICT,
            flight_date varchar(10) NOT NULL,
            flight_airport varchar(15) NOT NULL
            );""",

    """ CREATE TABLE IF NOT EXISTS WORKERS_PER_FLIGHT(
            flight_id integer NOT NULL,
            worker_id integer NOT NULL,
            ord integer DEFAULT 0,
                CHECK (ord > 0),
            FOREIGN KEY (flight_id) REFERENCES FLIGHTS(flight_id),
            FOREIGN KEY (worker_id) REFERENCES AIRLINE_WORKERS(worker_id),
            PRIMARY KEY (flight_id,worker_id)
            );"""

]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://itucs:itucspw@localhost:32768/itucsdb"  # os.getenv("DATABASE_URL")
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
initialize(url)
