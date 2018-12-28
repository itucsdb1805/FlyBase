Parts Implemented by Ahmed Burak Gulhan
================================

Functions in user.py
------------



execute_sql()
^^^^^^^^
.. code-block:: python
  def execute_sql(command):
      print("executing...")
      print(command)
      #command = """UPDATE COUNTRIES SET country_name = Turkey WHERE country_id = 1;"""
      try:
              url = os.getenv("DATABASE_URL")  #url = "postgres://itucs:itucspw@localhost:32769/itucsdb"#
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
  
This function takes an string which contains PostgreSQL code and executes it.  The first try, except loop (implemented by member Ahmed) tries to connect to the sql server.  If successful it executes the sql code and if there is any query result from this code it saves it the variable “data” then moves on to the seconds try, except loop.  If unsuccessful it returns -1.  The second try, except loop (implemented  by member Bulut) checks if the variable “data” is empty.  If it is then the value -2 is returned.  If “data” is not empty, the names of the columns are appended to the list (data) as the first item and data is returned.

Functions in views.py
------------

sqlgen_update()
^^^^^^^^
.. code-block:: python
  def sqlgen_update(table_name, column_names, variables, primary_key_count): #(string, list, list) !ID must be first item in lists. 
      command = "UPDATE " + table_name + " " + " SET "
      for index in range(primary_key_count,len(column_names)):#start from id_count in order to not change id
          if (variables[index] == "null"): 
              command += column_names[index] + " = NULL, "
          elif (variables[index] != ""):
              command += column_names[index] + " = '" + variables[index] + "', "
      command = command[:-2] #remove last character (,) from string
      if (primary_key_count == 1):
          command += " WHERE " + column_names[0] + " = '" + variables[0] + "';"
      elif (primary_key_count == 2):
          command += " WHERE " + column_names[0] + " = '" + variables[0] + "' AND " + column_names[1] + " = '" + variables[1] + "';"
      else:
          print("error primary_id_count must be 1 or 2")
      print("result: ")
      print(command)

  return command

This function is located in views.py
This function is used to generate an sql update command and return it as a string.  The inputs are:
table_name: a string with the name of the table being updated.
column_names: name of the columns of the table as a list of string.  Must include all column names, with the first item being the primary ID(s).
variables: a list of strings with the new values of the list’s columns.  The values must be in the same index as the input column_names with respect to it’s column name.  If the value will not be changed, then it must be an empty string “”.  If the value is being set to null the the value must be the string “null”.
primary_key_count: an integer.  Must be 1 or 2.  Used to generate an sql command with respect to how many primary keys the table has.  If the primary key count in a table is 1 then the value of this input is 1.  If it is 2 then the value of this input is 2.
The function makes a variable called “command” with it’s value initially set as “UPDATE” + table_name + “SET”.  This is the beginning of every sql update command.  Then the function enters a for loop where the variable “command” is appended with the parts where the columns names are being updated with respect to the variables.  This part checks if the variables are and empty string or “null” and appends accordingly.  After this for loop the “WHERE” part of the sql code is added to “command”.  This part checks the variable primary_key_count and acts accordingly.  Then the variable “command” which contains the full sql code is returned.

my_function()
^^^^^^^^
.. code-block:: python
  mycode

explanation of code

