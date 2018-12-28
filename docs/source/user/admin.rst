Admin
================================

Admin Login
--------

.. figure:: photos/admin/admin_login.jpg


This is how admin logs in.


Admin Page
--------

.. figure:: photos/admin/admin_page.jpg

    
Admin's page. All the options admin has. 


Intermediate Page of Selecting Tables for Operations
--------

.. figure:: photos/admin/table_selecting.jpg

    
After clicking options (add, delete, update, view) this page shows up and admin selects the table to implement the option he has just chosen. 

.. figure:: photos/admin/table_names.jpg


These are the names of the tables. Admin can only change main tables.


Option 1: Add
--------

.. figure:: photos/admin/add/add_aircraft.jpg


Add an aircraft. These are the necessary info that website asks from admin so that a new aircraft can be added to the database.

.. figure:: photos/admin/add/add_booking.jpg


Add a booking. These are the necessary info that website asks from admin so that a new booking can be added to the database.

.. figure:: photos/admin/add/add_flight.jpg


Add an flight. These are the necessary info that website asks from admin so that a new flight can be added to the database.

.. figure:: photos/admin/add/add_passenger.jpg


Add a passenger. These are the necessary info that website asks from admin so that a new passenger can be added to the database.

.. figure:: photos/admin/add/add_route.jpg


Add a route. These are the necessary info that website asks from admin so that a new route can be added to the database.

.. figure:: photos/admin/add/add_staff.jpg


Add a staff. These are the necessary info that website asks from admin so that a new staff can be added to the database.


Option 2: Delete
--------

Here, website only asks necessary id information to delete a booking/flight/passenger/route/aircraft/staff from the database. More complicated delete combination (since there are hundreds) can be handled from the 5th option which is entering direct sql query. 

.. figure:: photos/admin/delete/delete_aircraft.jpg


Delete an aircraft. This is the necessary info that website asks from admin so that a new aircraft can be deleted to the database. Only aircraft_id is necessary. 

.. figure:: photos/admin/delete/delete_booking.jpg


Delete a booking. These are the necessary info that website asks from admin so that a new booking can be deleted to the database. Only passenger_id and flight_id are necessary. 

.. figure:: photos/admin/delete/delete_flight.jpg


Delete a flight. This is the necessary info that website asks from admin so that a new flight can be deleted to the database. Only flight_id is necessary. 

.. figure:: photos/admin/delete/delete_passenger.jpg


Delete a passenger. This is the necessary info that website asks from admin so that a new passenger can be deleted to the database. Only passenger_id is necessary. 

.. figure:: photos/admin/delete/delete_route.jpg


Delete a route. This is the necessary info that website asks from admin so that a new route can be deleted to the database. Only route_id is necessary. 

.. figure:: photos/admin/delete/delete_staff.jpg


Delete a staff. This is the necessary info that website asks from admin so that a new staff can be deleted to the database. Only staff_id is necessary. 


Option 3: Update
--------

Here, website asks information regarding to what is going to be updated. Only filled forms are executed in the update operation. Empty forms are considered as they are not going to change.

.. figure:: photos/admin/update/update_aircraft.jpg


Update an aircraft. Admin fills out what is needed to change in the Aircrafts table. 

.. figure:: photos/admin/update/update_booking.jpg


Update a booking. Admin fills out what is needed to change in the Bookings table. 

.. figure:: photos/admin/update/update_flight.jpg


Update an flight. Admin fills out what is needed to change in the Flights table. 

.. figure:: photos/admin/update/update_passenger.jpg


Update a passenger. Admin fills out what is needed to change in the Passenger table. 

.. figure:: photos/admin/update/update_route.jpg


Update a route. Admin fills out what is needed to change in the Routes table. 

.. figure:: photos/admin/update/update_staff.jpg


Update a staff. Admin fills out what is needed to change in the Staff table. 


Option 4: View
--------

Here, website shows the rows of the table that has been chosen. 

.. figure:: photos/admin/update/update_aircraft.jpg


These are the aircrafts in the database.

.. figure:: photos/admin/update/update_booking.jpg


These are the aircrafts in the database.

.. figure:: photos/admin/delete/update_flight.jpg


These are the flights in the database.

.. figure:: photos/admin/update/update_passenger.jpg


These are the passengers in the database. First 2 are the members Bulut and Ahmed.

.. figure:: photos/admin/update/update_route.jpg


These are the routes in the database. 

.. figure:: photos/admin/update/update_staff.jpg


These are the staff in the database. 


Option 5: SQL Query
--------

This option is designed for complicated sql queries that admin would like to apply and cannot do with previous options.

.. figure:: photos/admin/sql_code_enter.jpg


This box is where admin enters the query. 

Let's see an example. 

.. figure:: photos/admin/example_sql.jpg

We try to view flights that take more than 8 hours.

.. figure:: photos/admin/example_sql_result.jpg

These are the flights that are very tiring to fly in the economy class.

