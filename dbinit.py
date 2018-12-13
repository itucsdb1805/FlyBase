import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """ CREATE TABLE IF NOT EXISTS COUNTRIES(
            country_id serial PRIMARY KEY,
            country_name varchar(50) UNIQUE NOT NULL
            );""",

    " INSERT INTO COUNTRIES (country_name) VALUES ('Turkey');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('France');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Germany');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('United States of America');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Russia');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Latvia');",

    """ CREATE TABLE IF NOT EXISTS TEST(
            test_id serial PRIMARY KEY,
            test_date date NOT NULL
            );""",



    """ CREATE TABLE IF NOT EXISTS AIRLINES(
            airline_id serial PRIMARY KEY,
            airline_name varchar(20) UNIQUE NOT NULL
            );""",

    " INSERT INTO AIRLINES (airline_name) VALUES ('THY1');",
    " INSERT INTO AIRLINES (airline_name) VALUES ('THY2');",
    " INSERT INTO AIRLINES (airline_name) VALUES ('THY3');",

    """ CREATE TABLE IF NOT EXISTS AIRPORTS(
            airport_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            airport_name varchar(30) NOT NULL,
            city_name varchar(30) NOT NULL,
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (1, 'Ataturk Airport', 'Istanbul');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (1, 'Sabiha Gokcen Airport', 'Istanbul');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (1, 'Esenboga Airport', 'Ankara');",


    """ CREATE TABLE IF NOT EXISTS AIRCRAFTS(
            aircraft_id serial PRIMARY KEY,
            airline_id integer NOT NULL,
            capacity integer NOT NULL,
            company_name varchar(20) NOT NULL,
            model_name varchar(20) NOT NULL,
            maximum_range integer NOT NULL,
            year_produced integer NOT NULL,
            FOREIGN KEY (airline_id) REFERENCES AIRLINES(airline_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range, year_produced) VALUES (1, 300, 'Boeing', '737', 2500, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range, year_produced) VALUES (1, 400, 'Airbus', 'A320', 2300, 2002);",

    """ CREATE TABLE IF NOT EXISTS ROUTES(
            route_id serial PRIMARY KEY,
            dep_airport_id integer NOT NULL,
            arr_airport_id integer NOT NULL,
            route_name varchar(20) NOT NULL,
            distance integer NOT NULL,
            number_of_flights integer DEFAULT 0,
            number_of_airlines integer NOT NULL,
            number_of_passengers integer DEFAULT 0,
            FOREIGN KEY (dep_airport_id) REFERENCES AIRPORTS(airport_id) ON DELETE RESTRICT,
            FOREIGN KEY (arr_airport_id) REFERENCES AIRPORTS(airport_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance, number_of_airlines) VALUES (1, 3, 'IST-ESB', 600, 2);",
    " INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance, number_of_airlines) VALUES (2, 3, 'SBH-ESB', 600, 3);",


    """ CREATE TABLE IF NOT EXISTS PASSENGERS(
            passenger_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            passenger_name varchar (30) NOT NULL,
            passenger_last_name varchar (30) NOT NULL,
            email varchar (50),
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            gender  varchar (1) NOT NULL
                CHECK (gender IN ( 'F' , 'M' ) ),
            passport_id integer NOT NULL UNIQUE
            file_data BYTEA
            );""",

    " INSERT INTO PASSENGERS (country_id, passenger_name, passenger_last_name) VALUES (1, 'Bulut', 'Ozler');",
    " INSERT INTO PASSENGERS (country_id, passenger_name, passenger_last_name) VALUES (4, 'Chandler', 'Bing');",


    """ CREATE TABLE IF NOT EXISTS STAFF(
            staff_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            airline_id integer NOT NULL,
            job_title varchar (20) NOT NULL,
            staff_name varchar (30) NOT NULL,
            staff_last_name varchar (30) NOT NULL,
            start_date varchar (10) NOT NULL,
            gender  varchar (1) NOT NULL
                CHECK (gender IN ( 'F' , 'M' ) ),
            file_data BYTEA
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id),
            FOREIGN KEY (airline_id) REFERENCES AIRLINES(airline_id)
            );""",

    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date) VALUES (1, 2, 'Pilot', 'John', 'Doe', '2017-10-09');",



    """ CREATE TABLE IF NOT EXISTS FLIGHTS(
            flight_id serial PRIMARY KEY,
            aircraft_id integer NOT NULL,
            route_id integer NOT NULL,
            departure_date varchar (10) NOT NULL,
            arrival_date varchar (10) NOT NULL,
            fuel_consumption integer NOT NULL,
            duration integer NOT NULL,
            average_altitude integer NOT NULL,
            FOREIGN KEY (aircraft_id) REFERENCES AIRCRAFTS(aircraft_id) ON DELETE RESTRICT,
            FOREIGN KEY (route_id) REFERENCES ROUTES(route_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO FLIGHTS (aircraft_id, route_id, departure_date, arrival_date, fuel_consumption, duration, average_altitude) VALUES (1, 2, '2019-01-02', '2019-01-03', 150000, 10, 12000);",


    """ CREATE TABLE IF NOT EXISTS BOOKINGS(
            flight_id integer NOT NULL,
            passenger_id integer NOT NULL,
            payment_type varchar (15) NOT NULL,
            miles_used integer,
            seat varchar (3) NOT NULL,
            class_of_seat varchar (15) NOT NULL,
            fare integer NOT NULL,
            FOREIGN KEY (flight_id) REFERENCES FLIGHTS(flight_id) ON DELETE RESTRICT,
            FOREIGN KEY (passenger_id) REFERENCES PASSENGERS(passenger_id) ON DELETE RESTRICT,
            PRIMARY KEY (flight_id, passenger_id)
            );"""

    " INSERT INTO BOOKINGS (flight_id, passenger_id, payment_type, miles_used, seat, class_of_seat, fare) VALUES (1, 2,  'Credit Card', 200, '42F', 'First Class', 300);",

""" CREATE TABLE IF NOT EXISTS USERS(
            username varchar NOT NULL UNIQUE CHECK (char_length(username) >= 5 AND char_length(username) <= 15)
            password varchar NOT NULL,
            passport_id integer NOT NULL
            );"""
]

INIT_STATEMENTS2 = ["TRUNCATE  flights,  aircrafts, airlines, routes,  passengers CASCADE;"]

INIT_STATEMENTS3 = [













]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        #for statement in INIT_STATEMENTS2:
            #cursor.execute(statement)
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    url = "postgres://itucs:itucspw@localhost:32769/itucsdb"#os.getenv("DATABASE_URL")
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
initialize(url)
