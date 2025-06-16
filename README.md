## Project Overview: Coursework for Lapin AMK, Edistynyt Tiedonhallinta (Lapland UAS, Advanced Data Management) through Open UAS studies

This project connects to an MQTT server, collects sensor data, and populates a structured SQL database with it. Below are key components and instructions:

### Database Initialization

- `mqtt_sensor_database.txt` contains the SQL script to create the necessary database schema for the project.

### Sensor Dimension Insertion

- Sensor metadata can be inserted using either:
  - `insert_sensors.py` (default)
  - `insert_sensors_alphabetical.py` (excludes sensors starting with a number)

**Note:**  
- `insert_sensors.py` may lead to more insertion errors because some sensor IDs starting with a letter may conflict with MQTT input.
- `insert_sensors_alphabetical.py` handles this more gracefully by skipping sensors that start with numbers.

###  Data Collection

- Run `main.py` to begin real-time ingestion of MQTT data into the database.
- Be mindful:
  - `insert_sensors.py` may cause more database insertion errors.
  - `insert_sensors_alphabetical.py` typically allows for smoother data integration.
  - Some insert errors will still occur—see the example queries below for troubleshooting.

### Querying the Database

- You can query the database from the console.
- `Query.py` provides several example queries for reference and exploration.

