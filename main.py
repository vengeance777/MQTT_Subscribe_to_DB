import certifi
import json
from datetime import datetime
import paho.mqtt.client as mqtt
from sqlalchemy import text
from db import get_db

def save_to_db(sensor_id, sensor_value, timestamp):
    with get_db() as _db:
        try:
            insert_data_query = """
            INSERT INTO sensor_data (sensor_id, sensor_value, timestamp)
            VALUES (:sensor_id, :sensor_value, :timestamp)
            """
            _db.execute(text(insert_data_query), {
                'sensor_id': sensor_id,
                'sensor_value': sensor_value,
                'timestamp': timestamp
            })
            _db.commit()
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error inserting sensor data: {e}")

def save_to_db_time(timestamp):
    with get_db() as _db:
        try:
            # Insert query including the parsed components
            insert_data_query = """
            INSERT INTO date_dim (
                timestamp, year, month, iso_week, day, hour, minute, second, microsecond
            ) VALUES (
                :timestamp, 
                :year, 
                :month, 
                :iso_week, 
                :day, 
                :hour, 
                :minute, 
                :second, 
                :microsecond
            )
            ON DUPLICATE KEY UPDATE timestamp=VALUES(timestamp)
            """
            _db.execute(text(insert_data_query), {
                'timestamp': timestamp,
                'year': timestamp.year,
                'month': timestamp.month,
                'iso_week': timestamp.isocalendar()[1],
                'day': timestamp.day,
                'hour': timestamp.hour,
                'minute': timestamp.minute,
                'second': timestamp.second,
                'microsecond': timestamp.microsecond
            })
            _db.commit()
            print("Date data saved successfully.")
        except Exception as e:
            print(f"Error inserting date data: {e}")


# Example usage:
# load_metadata_and_populate_sensor_dim('coolbox_metadata.json')
# save_to_db('some_sensor_id', 23.45, '2024-07-30 11:57:37')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("subscribe_address_here")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        ts_in_sec = payload['ts'] / 1000  # Using float division to include milliseconds
        dt = datetime.fromtimestamp(ts_in_sec)
        device = tuple(payload['d'].keys())[0]
        sensor_data = payload['d'][device]
        sensor = tuple(sensor_data.keys())[0]
        value = sensor_data[sensor]['v']
        print(sensor, value, dt)

        save_to_db_time(dt)  # Ensure the date entry is added before the sensor data entry
        save_to_db(sensor, value, dt)

    except Exception as e:
        print(f"Error processing message: {e}")

mqttc = mqtt.Client(protocol=mqtt.MQTTv5)  # Ensure proper protocol version is used
mqttc.on_connect = on_connect
mqttc.on_message = on_message


# Setting username and password for the MQTT client
mqttc.username_pw_set(username="username", password="password")

# Configuring TLS/SSL settings
mqttc.tls_set(ca_certs=certifi.where())

# Connecting to the MQTT server
mqttc.connect("mqttserver", port=port, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and #handles reconnecting.
# Other loop() Functions are available that give a threaded interface and a #manual interface.
mqttc.loop_forever()



""""def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        print(f"Received message: {payload}")  # 
    except Exception as e:
        print(f"Failed to parse payload: {e}")"""
