1. mqtt_sensor_database.txt is written in sql and it creates database required for the project
   
3. sensors to database dimension can be inserted from insert_sensors.py or insert_sensors_alphabetical.py

   insert_sensors_alphabetical.py contains sensors that DOES NOT start with a number. By default, insert_sensors.py is used.
   
4. main.py starts inserting data from mqtt server to database
   When populatng dimension: 
   if insert_sensors.py is used, there are more insertion errors because mqtt server tries to insert data that starts with a letter
   insert_sensors_alphabetical.py is able to insert more data because of non-numeric requirement
   There are still some errors (see queries)

5. Queries can be done from console, Query.py contains some example queries. 
