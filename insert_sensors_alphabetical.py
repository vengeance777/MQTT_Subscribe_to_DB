import json
from sqlalchemy import text  # Correct import for text
from db import get_db

# 1. Lue coolbox_metadata.json-tiedoston sisältö
try:
    with open('coolbox_metadata.json', 'r', encoding='UTF-8') as config_file:
        metadata = json.loads(config_file.read())
    with get_db() as _db:
        devices = metadata['devices']
        device_ids = devices.keys()
        print("Starting to process devices...")

        for device_id in device_ids:
            device = devices.get(device_id)
            device_name = device['sd']
            sensors = device['sensors']
            if sensors == {}:
                continue
            for sensor_id in sensors.keys():
                sensor = sensors.get(sensor_id)
                if 'unit' not in sensor:
                    continue
                sensor_description = sensor['sd']
                _query_str = """
                INSERT INTO sensor_dim(sensor_id, device_id, device_name, sensor_description, sensor_type, measurement_unit)
                VALUES(:sensor_id, :device_id, :device_name, :sensor_description, :sensor_type, :measurement_unit)
                ON DUPLICATE KEY UPDATE
                    device_id = VALUES(device_id),
                    device_name = VALUES(device_name),
                    sensor_description = VALUES(sensor_description),
                    measurement_unit = VALUES(measurement_unit);
                """
                print(f"Inserting/Updating sensor_id: {sensor_id}")
                _db.execute(text(_query_str), {
                    'sensor_id': sensor_id,
                    'device_id': device_id,
                    'device_name': device_name,
                    'sensor_description': sensor_description,
                    'measurement_unit': sensor['unit']
                })
        _db.commit()
        print("All device data processed and committed.")
except Exception as e:
    print(f"An error occurred: {e}")