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
            if not device_id.isnumeric():
                continue
            device = devices.get(device_id)
            device_name = device['sd']
            sensors = device['sensors']
            if sensors == {}:
                continue
            sensor_ids = sensors.keys()
            for sensor_id in sensor_ids:
                sensor = sensors.get(sensor_id)
                if 'unit' not in sensor:
                    continue
                sensor_description = sensor['sd']
                # on duplicate update because the json file has one case for duplicate value
                _query_str = """
                INSERT INTO sensor_dim(sensor_id, device_id, device_name, sensor_description, device_unit)
                VALUES(:sensor_id, :device_id, :device_name, :sensor_description, :device_unit)
                ON DUPLICATE KEY UPDATE
                    device_id = VALUES(device_id),
                    device_name = VALUES(device_name),
                    sensor_description = VALUES(sensor_description),
                    device_unit = VALUES(device_unit);
                """
                print(f"Inserting/Updating sensor_id: {sensor_id}")
                _db.execute(text(_query_str), {
                    'sensor_id': sensor_id,
                    'device_id': device_id,
                    'device_name': device_name,
                    'sensor_description': sensor_description,
                    'device_unit': sensor['unit']
                })
        _db.commit()
        print("All device data processed and committed.")


except Exception as e:
    print(f"An error occurred: {e}")
    _db.rollback()
    raise e
