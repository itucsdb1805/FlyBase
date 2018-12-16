import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """ CREATE TABLE IF NOT EXISTS COUNTRIES(
            country_id serial PRIMARY KEY,
            country_name varchar(50) UNIQUE NOT NULL
            );""",

    " INSERT INTO COUNTRIES (country_name) VALUES ('Turkey');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('China');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Germany');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('United States of America');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Russia');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Australia');",
    " INSERT INTO COUNTRIES (country_name) VALUES ('Brazil');",

    """ CREATE TABLE IF NOT EXISTS TEST(
            test_id serial PRIMARY KEY,
            test_date date NOT NULL
            );""",



    """ CREATE TABLE IF NOT EXISTS AIRLINES(
            airline_id serial PRIMARY KEY,
            airline_name varchar(20) UNIQUE NOT NULL
            );""",

    " INSERT INTO AIRLINES (airline_name) VALUES ('Pacific Airlines');",
    " INSERT INTO AIRLINES (airline_name) VALUES ('Eurasia Airlines');",
    " INSERT INTO AIRLINES (airline_name) VALUES ('South Pole Airlines');",
    " INSERT INTO AIRLINES (airline_name) VALUES ('North Blue Airlines');",

    """ CREATE TABLE IF NOT EXISTS AIRPORTS(
            airport_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            airport_name varchar(40) NOT NULL,
            city_name varchar(20) NOT NULL,
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (1, 'Istanbul Ataturk Airport', 'Istanbul');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (1, 'Esenboga International Airport', 'Ankara');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (2, 'Beijing Capital International Airport', 'Beijing');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (3, 'Frankfurt Airport', 'Frankfurt');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (4, 'Los Angeles International Airport', 'Los Angeles');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (4, 'John F. Kennedy International Airport', 'New York City');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (5, 'Pulkovo Airport', 'Saint Petersburg');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (6, 'Sydney Airport', 'Sydney');",
    " INSERT INTO AIRPORTS (country_id, airport_name, city_name) VALUES (7, 'Rio de Janeiro International Airport', 'Rio de Janeiro');",

    """ CREATE TABLE IF NOT EXISTS AIRCRAFTS(
            aircraft_id serial PRIMARY KEY,
            airline_id integer NOT NULL,
            capacity integer NOT NULL CHECK (capacity BETWEEN 200 and 800),
            company_name varchar(20) NOT NULL,
            model_name varchar(20) NOT NULL,
            maximum_range_km integer NOT NULL,
            year_produced integer NOT NULL CHECK (year_produced BETWEEN  1980 and 2018 ),
            FOREIGN KEY (airline_id) REFERENCES AIRLINES(airline_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 300, 'Boeing', '737', 3500, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 400, 'Airbus', 'A320', 3300, 2010);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 600, 'Airbus', 'A350', 5300, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 400, 'Airbus', 'A320', 3300, 2009);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 500, 'Airbus', 'A350', 5300, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 700, 'Airbus', 'A380', 6000, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 500, 'Airbus', 'A330', 4300, 2004);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (1, 700, 'Boeing', '787', 6000, 1999);",

    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 600, 'Boeing', '777', 5400, 2009);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 700, 'Boeing', '787', 6000, 2005);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 400, 'Airbus', 'A320', 3300, 2001);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 700, 'Boeing', '787', 6000, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 300, 'Boeing', '737', 3500, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 400, 'Boeing', '747', 4500, 2003);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (2, 600, 'Boeing', '777', 5400, 2004);",

    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 600, 'Airbus', 'A350', 5300, 2004);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 500, 'Boeing', '767', 2700, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 400, 'Boeing', '747', 4500, 2003);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 400, 'Airbus', 'A320', 3300, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 600, 'Airbus', 'A350', 5300, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 500, 'Boeing', '767', 4800, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (3, 700, 'Boeing', '787', 6000, 2003);",

    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 600, 'Boeing', '777', 5400, 1999);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 600, 'Boeing', '777', 5400, 1996);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 500, 'Boeing', '767', 4800, 2009);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 700, 'Airbus', 'A380', 6000, 2002);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 600, 'Boeing', '777', 5400, 2004);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 400, 'Boeing', '747', 4500, 2003);",
    " INSERT INTO AIRCRAFTS (airline_id, capacity, company_name, model_name, maximum_range_km, year_produced) VALUES (4, 700, 'Airbus', 'A380', 6000, 2009);",

    """ CREATE TABLE IF NOT EXISTS ROUTES(
            route_id serial PRIMARY KEY,
            dep_airport_id integer NOT NULL,
            arr_airport_id integer NOT NULL,
            route_name varchar(10) NOT NULL,
            distance_km integer NOT NULL,
            number_of_airlines integer,
            intercontinental varchar (1) NOT NULL CHECK (intercontinental in ('y', 'Y', 'n', 'N')),
            active_since integer NOT NULL CHECK (active_since BETWEEN 1950 and 2018 ),
            altitude_feet integer NOT NULL CHECK (altitude_feet BETWEEN 30000 and 40000),
            FOREIGN KEY (dep_airport_id) REFERENCES AIRPORTS(airport_id) ON DELETE RESTRICT,
            FOREIGN KEY (arr_airport_id) REFERENCES AIRPORTS(airport_id) ON DELETE RESTRICT
            );""",

    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (1, 2, 'IST-ESB', 600, 1, 'n', 1960, 36000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (2, 1, 'ESB-IST', 600, 1, 'n', 1960, 36000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (1, 3, 'IST-PEK', 4000, 1, 'y', 1988, 39000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 1, 'PEK-IST', 4000, 1, 'y', 1988, 39000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (1, 4, 'IST-FRA', 2500, 1, 'n', 1968, 37000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (4, 2, 'FRA-ESB', 2500, 1, 'y', 1978, 37000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (1, 6, 'IST-JFK', 3800, 1, 'Y', 1975, 34000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (6, 1, 'JFK-IST', 3800, 1, 'Y', 1975, 34000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (1, 7, 'IST-LED', 2800, 1, 'N', 1973, 32000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (7, 2, 'LED-ESB', 2900, 1, 'N', 1978, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 7, 'PEK-LED', 2300, 2, 'N', 1983, 38000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (7, 3, 'LED-PEK', 2300, 2, 'N', 1988, 38000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 8, 'PEK-SYD', 4300, 1, 'Y', 1984, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (8, 3, 'SYD-PEK', 4300, 1, 'Y', 1984, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 5, 'PEK-LAX', 5300, 2, 'Y', 1994, 37000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (5, 3, 'LAX-PEK', 5300, 2, 'Y', 1994, 37000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 9, 'PEK-GIG', 5700, 1, 'Y', 1998, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (9, 3, 'GIG-PEK', 5700, 1, 'Y', 1997, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (3, 4, 'PEK-FRA', 5600, 1, 'Y', 1993, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (4, 3, 'FRA-PEK', 5600, 1, 'Y', 1994, 34000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (4, 6, 'FRA-JFK', 4600, 1, 'Y', 1963, 38000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (6, 4, 'JFK-FRA', 4600, 1, 'Y', 1954, 39000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (4, 7, 'FRA-LED', 3400, 1, 'Y', 1973, 38000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (7, 4, 'LED-FRA', 3400, 1, 'Y', 1984, 39000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (4, 9, 'FRA-GIG', 4400, 1, 'Y', 1977, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (9, 4, 'GIG-FRA', 4400, 1, 'Y', 1981, 36000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (5, 6, 'LAX-JFK', 3000, 1, 'N', 1957, 35000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (6, 5, 'JFK-LAX', 3000, 1, 'N', 1955, 36000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (5, 8, 'LAX-SYD', 5500, 1, 'Y', 1977, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (8, 5, 'SYD-LAX', 5500, 1, 'Y', 1975, 32000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (5, 9, 'LAX-GIG', 2500, 1, 'Y', 1967, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (9, 5, 'GIG-LAX', 2500, 1, 'Y', 1965, 32000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (6, 7, 'JFK-LED', 4500, 2, 'Y', 1967, 36000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (7, 6, 'LED-JFK', 4500, 2, 'Y', 1965, 37000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (6, 9, 'JFK-GIG', 3700, 1, 'Y', 1968, 32000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (9, 6, 'GIG-JFK', 3700, 1, 'Y', 1963, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (7, 8, 'LED-SYD', 5500, 1, 'Y', 1987, 33000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (8, 7, 'SYD-LED', 5500, 1, 'Y', 1985, 34000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (8, 9, 'SYD-GIG', 5200, 1, 'Y', 1987, 39000);""",
    """ INSERT INTO ROUTES (dep_airport_id, arr_airport_id, route_name, distance_km, number_of_airlines, intercontinental, active_since, altitude_feet) VALUES 
                           (9, 8, 'GIG-SYD', 5200, 1, 'Y', 1985, 39000);""",


    """ CREATE TABLE IF NOT EXISTS PASSENGERS(
            passenger_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            passport_id integer NOT NULL UNIQUE CHECK (passport_id BETWEEN 10000 and 99999),
            passenger_name varchar (20) NOT NULL,
            passenger_last_name varchar (20) NOT NULL,
            email varchar (50),
            gender  varchar (5) NOT NULL CHECK (gender IN ( 'F' , 'M' , 'OTHER') ),
            file_data BYTEA,
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id) ON DELETE RESTRICT
            );""",

    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (1, 10001, 'Bulut', 'Ozler', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (1, 10002, 'Ahmed', 'Gulhan', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (2, 20001, 'Yao', 'Ming', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (2, 20002, 'He', 'He', 'F');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (3, 30001, 'Niklas', 'Schule', 'OTHER');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (3, 30002, 'Maria', 'Müller', 'F');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (4, 40001, 'Frank', 'Whistler', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (4, 40002, 'Rositta', 'Angelov', 'F');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (5, 50001, 'Sergey', 'Pushkin', 'OTHER');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (5, 50002, 'Natalie', 'Rasputin', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (6, 60001, 'James', 'McAvoy', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (6, 60002, 'Jill', 'Green', 'F');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (7, 70001, 'Matthias', 'Josue', 'M');",
    " INSERT INTO PASSENGERS (country_id, passport_id, passenger_name, passenger_last_name, gender) VALUES (7, 70002, 'Veronica', 'Austin', 'F');",

    """ CREATE TABLE IF NOT EXISTS STAFF(
            staff_id serial PRIMARY KEY,
            country_id integer NOT NULL,
            airline_id integer NOT NULL,
            job_title varchar (20) NOT NULL CHECK (job_title IN ('Pilot', 'Cabin Crew')),
            staff_name varchar (20) NOT NULL,
            staff_last_name varchar (20) NOT NULL,
            start_date date NOT NULL,
            gender  varchar (5) NOT NULL CHECK (gender IN ( 'F' , 'M' , 'OTHER') ),
            file_data BYTEA,
            FOREIGN KEY (country_id) REFERENCES COUNTRIES(country_id),
            FOREIGN KEY (airline_id) REFERENCES AIRLINES(airline_id)
            );""",

    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 1, 'Pilot', 'Goksel', 'Sezen', '2017-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (5, 1, 'Pilot', 'Maria', 'Kasparov', '2015-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 1, 'Pilot', 'Gerd', 'Müller', '2012-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 1, 'Pilot', 'Vedat', 'Yatkin', '2017-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (5, 1, 'Pilot', 'Joanna', 'Veledov', '2015-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 1, 'Pilot', 'Hans', 'Stadter', '2012-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 1, 'Pilot', 'Selim', 'Altin', '2017-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (5, 1, 'Pilot', 'Valerina', 'Vurken', '2015-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 1, 'Pilot', 'Mesut', 'Sebastian', '2012-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 1, 'Pilot', 'Faruk', 'Sevilen', '2017-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (5, 1, 'Pilot', 'Andrey', 'Arshavin', '2015-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 1, 'Pilot', 'Melb', 'Ausstadt', '2012-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (4, 2, 'Pilot', 'John', 'Doe', '2017-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 2, 'Pilot', 'Helga', 'Obst', '2014-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (6, 2, 'Pilot', 'Steven', 'Lightbear', '2011-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 2, 'Pilot', 'Helarin', 'Bellov', '2014-10-09', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (6, 2, 'Pilot', 'Stuart', 'Mill', '2011-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (4, 2, 'Pilot', 'Ian', 'Perry', '2017-11-01', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (4, 2, 'Pilot', 'Joey', 'Tribbiani', '2014-01-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (2, 2, 'Pilot', 'Chen', 'Choi', '2012-02-09', 'OTHER');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 2, 'Pilot', 'Sugdem', 'Himmetoglu', '2005-10-11', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (5, 3, 'Pilot', 'Derbishev', 'Duravski', '2017-11-01', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (3, 3, 'Pilot', 'Toni', 'Broos', '2014-01-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (2, 3, 'Pilot', 'Xeng', 'Chi', '2012-02-09', 'OTHER');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (1, 4, 'Pilot', 'Tugce', 'Basaran', '2005-10-11', 'F');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (4, 4, 'Pilot', 'Chesley', 'Sullenberger', '2000-10-09', 'M');",
    " INSERT INTO STAFF (country_id, airline_id, job_title, staff_name, staff_last_name, start_date, gender) VALUES (7, 4, 'Pilot', 'Jurado', 'Iglesias', '2012-05-09', 'OTHER');",


    """ CREATE TABLE IF NOT EXISTS FLIGHTS(
            flight_id serial PRIMARY KEY,
            route_id integer NOT NULL,
            aircraft_id integer NOT NULL,
            departure_date timestamp NOT NULL,
            arrival_date timestamp NOT NULL,
            fuel_liter integer NOT NULL CHECK (fuel_liter BETWEEN 15000 and 170000),
            time_hours integer NOT NULL CHECK (time_hours BETWEEN 1 and 10),
            number_passengers integer DEFAULT 0,
            FOREIGN KEY (aircraft_id) REFERENCES AIRCRAFTS(aircraft_id) ON DELETE CASCADE,
            FOREIGN KEY (route_id) REFERENCES ROUTES(route_id) ON DELETE CASCADE
            );""",

    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (1, 11, TIMESTAMP '2018-12-20 10:00:00', TIMESTAMP '2018-12-20 12:00:00', 31000, 2);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (2, 11, TIMESTAMP '2018-12-20 17:00:00', TIMESTAMP '2018-12-20 19:00:00', 32000, 2);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (3, 10, TIMESTAMP '2018-12-21 10:00:00', TIMESTAMP '2018-12-21 20:00:00', 150000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (4, 12, TIMESTAMP '2018-12-21 08:00:00', TIMESTAMP '2018-12-21 18:00:00', 145000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (5, 15, TIMESTAMP '2018-12-22 10:00:00', TIMESTAMP '2018-12-22 14:00:00', 55000, 4);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (6, 13, TIMESTAMP '2018-12-22 11:00:00', TIMESTAMP '2018-12-22 15:00:00', 60000, 4);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (7, 6, TIMESTAMP '2018-12-23 10:00:00', TIMESTAMP '2018-12-23 20:00:00', 140000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (8, 6, TIMESTAMP '2018-12-23 23:00:00', TIMESTAMP '2018-12-24 09:00:00', 150000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (9, 14, TIMESTAMP '2018-12-24 10:00:00', TIMESTAMP '2018-12-24 13:00:00', 47000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (10, 12, TIMESTAMP '2018-12-24 10:00:00', TIMESTAMP '2018-12-24 13:00:00', 53000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (11, 26, TIMESTAMP '2018-12-25 10:00:00', TIMESTAMP '2018-12-25 15:00:00', 75000, 5);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (12, 27, TIMESTAMP '2018-12-25 14:00:00', TIMESTAMP '2018-12-25 19:00:00', 89000, 5);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (13, 7, TIMESTAMP '2018-12-26 20:00:00', TIMESTAMP '2018-12-27 02:00:00', 90000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (14, 6, TIMESTAMP '2018-12-26 11:00:00', TIMESTAMP '2018-12-26 17:00:00', 80000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (15, 8, TIMESTAMP '2018-12-27 10:00:00', TIMESTAMP '2018-12-27 19:00:00', 140000, 9);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (16, 6, TIMESTAMP '2018-12-27 10:00:00', TIMESTAMP '2018-12-27 19:00:00', 130000, 9);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (17, 8, TIMESTAMP '2018-12-28 10:00:00', TIMESTAMP '2018-12-28 18:00:00', 130000, 8);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (18, 6, TIMESTAMP '2018-12-28 10:00:00', TIMESTAMP '2018-12-28 18:00:00', 140000, 8);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (19, 10, TIMESTAMP '2018-12-29 17:00:00', TIMESTAMP '2018-12-29 23:00:00', 100000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (20, 12, TIMESTAMP '2018-12-29 10:00:00', TIMESTAMP '2018-12-29 16:00:00', 100000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (21, 7, TIMESTAMP '2018-12-20 10:00:00', TIMESTAMP '2018-12-20 15:00:00', 50000, 5);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (22, 8, TIMESTAMP '2018-12-21 10:00:00', TIMESTAMP '2018-12-21 15:00:00', 50000, 5);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (23, 9, TIMESTAMP '2018-12-22 10:00:00', TIMESTAMP '2018-12-22 14:00:00', 55000, 4);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (24, 9, TIMESTAMP '2018-12-23 17:00:00', TIMESTAMP '2018-12-23 21:00:00', 50000, 4);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (25, 6, TIMESTAMP '2018-12-24 10:00:00', TIMESTAMP '2018-12-24 18:00:00', 150000, 8);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (26, 6, TIMESTAMP '2018-12-25 15:00:00', TIMESTAMP '2018-12-25 23:00:00', 140000, 8);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (27, 1, TIMESTAMP '2018-12-26 10:00:00', TIMESTAMP '2018-12-26 13:00:00', 45000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (28, 1, TIMESTAMP '2018-12-27 10:00:00', TIMESTAMP '2018-12-27 13:00:00', 44000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (29, 6, TIMESTAMP '2018-12-28 10:00:00', TIMESTAMP '2018-12-28 20:00:00', 150000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (30, 8, TIMESTAMP '2018-12-29 10:00:00', TIMESTAMP '2018-12-29 20:00:00', 150000, 10);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (31, 4, TIMESTAMP '2018-12-21 10:00:00', TIMESTAMP '2018-12-21 13:00:00', 43000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (32, 5, TIMESTAMP '2018-12-22 09:00:00', TIMESTAMP '2018-12-22 12:00:00', 51000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (33, 8, TIMESTAMP '2018-12-23 10:00:00', TIMESTAMP '2018-12-23 17:00:00', 130000, 7);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (34, 6, TIMESTAMP '2018-12-24 10:00:00', TIMESTAMP '2018-12-24 17:00:00', 120000, 7);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (35, 4, TIMESTAMP '2018-12-25 10:00:00', TIMESTAMP '2018-12-25 13:00:00', 150000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (36, 5, TIMESTAMP '2018-12-26 14:00:00', TIMESTAMP '2018-12-26 17:00:00', 48000, 3);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (37, 9, TIMESTAMP '2018-12-27 19:00:00', TIMESTAMP '2018-12-28 01:00:00', 83000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (38, 15, TIMESTAMP '2018-12-28 10:00:00', TIMESTAMP '2018-12-28 16:00:00', 73000, 6);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (39, 21, TIMESTAMP '2018-12-29 10:00:00', TIMESTAMP '2018-12-29 17:00:00', 110000, 7);""",
    """ INSERT INTO FLIGHTS (route_id, aircraft_id, departure_date, arrival_date, fuel_liter, time_hours) VALUES 
        (40, 22, TIMESTAMP '2018-12-25 10:00:00', TIMESTAMP '2018-12-25 17:00:00', 110000, 7);""",

    """ CREATE TABLE IF NOT EXISTS ROUTE_AIRLINE(
            route_id integer NOT NULL,
            airline_id integer NOT NULL, 
            FOREIGN KEY (airline_id) REFERENCES AIRLINES(airline_id) ON DELETE CASCADE,
            FOREIGN KEY (route_id) REFERENCES ROUTES(route_id) ON DELETE CASCADE,
            PRIMARY KEY (airline_id, route_id)
            );""",

    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (1, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (2, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (3, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (4, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (5, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (6, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (7, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (8, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (9, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (10, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (11, 4);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (12, 4);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (13, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (14, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (15, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (16, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (17, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (18, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (19, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (20, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (21, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (22, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (23, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (24, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (25, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (26, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (27, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (28, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (29, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (30, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (31, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (32, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (33, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (34, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (35, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (36, 1);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (37, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (38, 2);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (39, 3);",
    " INSERT INTO ROUTE_AIRLINE (route_id, airline_id) VALUES (40, 3);",

    """ CREATE TABLE IF NOT EXISTS STAFF_FLIGHT(
            flight_id integer NOT NULL,
            staff_id integer NOT NULL, 
            FOREIGN KEY (staff_id) REFERENCES STAFF(staff_id) ON DELETE CASCADE,
            FOREIGN KEY (flight_id) REFERENCES FLIGHTS(flight_id) ON DELETE CASCADE,
            PRIMARY KEY (staff_id, flight_id)
            );""",

    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (1, 13);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (2, 14);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (3, 15);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (4, 13);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (5, 14);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (6, 13);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (7, 3);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (8, 5);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (9, 16);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (10, 18);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (11, 25);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (12, 26);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (13, 2);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (14, 3);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (15, 4);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (16, 5);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (17, 6);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (18, 7);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (19, 15);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (20, 18);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (21, 3);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (22, 7);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (23, 13);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (24, 19);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (25, 4);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (26, 5);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (27, 6);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (28, 7);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (29, 1);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (30, 2);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (31, 3);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (32, 11);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (33, 9);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (34, 10);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (35, 11);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (36, 9);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (37, 19);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (38, 17);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (39, 23);",
    " INSERT INTO STAFF_FLIGHT (flight_id, staff_id) VALUES (40, 24);",


    """ CREATE TABLE IF NOT EXISTS BOOKINGS(
            flight_id integer NOT NULL,
            passenger_id integer NOT NULL,
            payment_type varchar (20) NOT NULL CHECK (payment_type IN ('Credit Card', 'Paypal', 'Cryptocurrency')),
            purchase_time timestamp NOT NULL,
            seat VARCHAR (3) NOT NULL,
            class_of_seat varchar (15) NOT NULL CHECK (class_of_seat IN ('Budget', 'Economy', 'Business', 'First Class')),
            fare integer NOT NULL CHECK (fare IN (100, 200, 300, 400)),
            FOREIGN KEY (flight_id) REFERENCES FLIGHTS(flight_id) ON DELETE RESTRICT,
            FOREIGN KEY (passenger_id) REFERENCES PASSENGERS(passenger_id) ON DELETE RESTRICT,
            PRIMARY KEY (flight_id, passenger_id)
            );"""


""" CREATE TABLE IF NOT EXISTS USERS(
            username varchar NOT NULL UNIQUE PRIMARY KEY  CHECK (char_length(username) >= 5 AND char_length(username) <= 15),
            password varchar NOT NULL,
            passport_id integer,
            FOREIGN KEY (passport_id) REFERENCES PASSENGERS(passport_id) ON UPDATE CASCADE 
            );""",

    " INSERT INTO USERS (username, password) VALUES ('admin', '$pbkdf2-sha256$29000$PIdwDqH03hvjXAuhlLL2Pg$B1K8TX6Efq3GzvKlxDKIk4T7yJzIIzsuSegjZ6hAKLk');",
    " INSERT INTO USERS (username, password, passport_id) VALUES ('bulutozler', '$pbkdf2-sha256$29000$OieEcM6Zk5Jybg1BaE3JmQ$BWg0IoexQvLKoS87giCdR2.2zHl1oOjaES2ajxTX/OM', 10001);",


]

INIT_STATEMENTS2 = [

    " DROP TABLE IF EXISTS BOOKINGS CASCADE ",
    " DROP TABLE IF EXISTS FLIGHTS CASCADE",
    " DROP TABLE IF EXISTS STAFF CASCADE",
    " DROP TABLE IF EXISTS AIRCRAFTS CASCADE",
    " DROP TABLE IF EXISTS AIRLINES CASCADE",
    " DROP TABLE IF EXISTS ROUTES CASCADE",
    " DROP TABLE IF EXISTS AIRPORTS CASCADE",
    " DROP TABLE IF EXISTS PASSENGERS CASCADE",
    " DROP TABLE IF EXISTS COUNTRIES CASCADE",
    " DROP TABLE IF EXISTS USERS CASCADE",
    " DROP TABLE IF EXISTS STAFF_FLIGHT CASCADE",
    " DROP TABLE IF EXISTS ROUTE_AIRLINE CASCADE"

]

INIT_STATEMENTS3 = [













]


def initialize(url):
    with dbapi2.connect(url) as connection:
        i = 0
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS2:
            cursor.execute(statement)
        for statement in INIT_STATEMENTS:
            print(i)
            i = i + 1
            cursor.execute(statement)

        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")  # url = "postgres://itucs:itucspw@localhost:32769/itucsdb"#
    print(url)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
initialize(url)
