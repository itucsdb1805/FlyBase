import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
""" CREATE TABLE IF NOT EXISTS COUNTRIES(
        country_id serial PRIMARY KEY,
        country_name varchar(50) NOT NULL
        );""",

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
        --airline_id integer NOT NULL REFERENCES AIRLINES(airline_ID) ON DELETE RESTRICT,
        job  varchar(15) NOT NULL
            CHECK (job IN ( 'pilot' , 'hostess' , 'other' ) ),
        photo varchar(50) DEFAULT './photos/default.jpg',
        FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
        );""",

""" CREATE TABLE IF NOT EXISTS FLIGHTS(
        flight_id serial PRIMARY KEY,
        --airline_id integer NOT NULL REFERENCES AIRLINES(airline_id) ON DELETE RESTRICT,
        --aircraft_id integer NOT NULL REFERENCES AIRLINES(aircraft_id) ON DELETE RESTRICT,
        --route_id integer NOT NULL REFERENCES AIRLINES(route_id) ON DELETE RESTRICT,
        departure timestamp,
        arrival timestamp,
        passenger_count integer DEFAULT 0,
        fuel_required decimal DEFAULT 0.0
        );"""

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
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
initialize(url)
