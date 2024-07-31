from sqlalchemy import text
from db import get_db

def query_yearly_transactions():
    year = int(input("Enter year: "))
    with get_db() as _db:
        _query_str = ("""
            SELECT COUNT(*) AS Sensor_observation_count
            FROM sensor_data
            INNER JOIN date_dim ON date_dim.timestamp = sensor_data.timestamp
            WHERE date_dim.year = :year
        """)
        _query = text(_query_str)
        rows = _db.execute(_query, {'year': year})
        data = rows.mappings().all()
        for row in data:
            print(f"Year: {year}, Transaction Count: {row['Sensor_observation_count']}")

def query_distinct_device_unit_count():
    with get_db() as _db:
        _query_str = ("""
    SELECT 
        sensor_dim.device_unit, 
        sensor_data.sensor_id, 
        MAX(sensor_data.sensor_value) AS maximum_sensor_value
    FROM sensor_data
    INNER JOIN sensor_dim ON sensor_data.sensor_id = sensor_dim.sensor_id
    GROUP BY sensor_dim.device_unit, sensor_data.sensor_id
    ORDER BY sensor_dim.device_unit;
""")
        _query = text(_query_str)
        rows = _db.execute(_query)
        data = rows.mappings().all()
        for row in data:
            print(f"device_unit: {row['device_unit']}, sensor_id: {row['sensor_id']}, maximum_sensor_value: {row['maximum_sensor_value']}")

def query_row_counts_and_error():
    with get_db() as _db:
        try:
            # Query to count rows in sensor_data
            sensor_data_count_query = "SELECT COUNT(*) AS count FROM sensor_data"
            sensor_data_count = _db.execute(text(sensor_data_count_query)).scalar()

            # Query to count rows in date_dim
            date_dim_count_query = "SELECT COUNT(*) AS count FROM date_dim"
            date_dim_count = _db.execute(text(date_dim_count_query)).scalar()

            # Calculate error percentage
            if date_dim_count > 0:
                error_percentage = abs(sensor_data_count - date_dim_count) / date_dim_count * 100
            else:
                error_percentage = 0  # Avoid division by zero

            # Print the row counts and error percentage
            print(f"Row count in sensor_data: {sensor_data_count}")
            print(f"Row count in date_dim: {date_dim_count}")
            print(f"Error percentage: {error_percentage:.2f}%")

        except Exception as e:
            print(f"Error querying row counts: {e}")


def query_row_counts_inserton_error():
    with get_db() as _db:
        try:
            query_str = """
                SELECT sensor_id, COUNT(*) AS count
                FROM sensor_data
                WHERE sensor_id IN ('190_128_0_IsLow', 'pvcurrent', 'pvvoltage')
                GROUP BY sensor_id
                UNION ALL
                SELECT 'Total' AS sensor_id, COUNT(*)
                FROM sensor_data
                WHERE sensor_id IN ('190_128_0_IsLow', 'pvcurrent', 'pvvoltage', 'L3');
            """
            query = text(query_str)
            rows = _db.execute(query).mappings().all()

            # Process and print the results
            for row in rows:
                print(f"Sensor ID: {row['sensor_id']}, Row count: {row['count']}")

        except Exception as e:
            print(f"Error querying row counts: {e}")


def query_distinct_sensor_counts():
    with get_db() as _db:
        try:
            # Query to count the number of distinct sensor_id values and list them
            distinct_sensor_count_query = """
                SELECT COUNT(DISTINCT sensor_id) AS distinct_sensor_count
                FROM sensor_data"""

            distinct_sensor_count_query_2 = """
                SELECT DISTINCT sensor_id
                FROM sensor_data"""

            sensor_data_count_query = """
                SELECT sensor_id, COUNT(*) AS count
                FROM sensor_data
                GROUP BY sensor_id"""

            total_count_query = """
                SELECT 'Total' AS sensor_id, COUNT(*) AS count
                FROM sensor_data """

            # Execute the queries
            distinct_sensor_count_rows = _db.execute(text(distinct_sensor_count_query)).mappings().all()
            #distinct_sensor_ids_rows = _db.execute(text(distinct_sensor_count_query_2)).mappings().all()
            sensor_data_count_rows = _db.execute(text(sensor_data_count_query)).mappings().all()
            total_count_rows = _db.execute(text(total_count_query)).mappings().all()

            # Print distinct sensor count
            for row in distinct_sensor_count_rows:
                print(f"Number of distinct sensor_id values: {row['distinct_sensor_count']}")

            # Extract and print distinct sensor IDs
            #sensor_id_list = [row['sensor_id'] for row in distinct_sensor_ids_rows]
            #print(f"Distinct sensor_id values: {sensor_id_list}")

            # Print sensor data counts for each sensor_id
            for row in sensor_data_count_rows:
                print(f"Sensor ID: {row['sensor_id']}, Count: {row['count']}")

            # Print total sensor data count
            for row in total_count_rows:
                print(f"Total number of sensor data entries: {row['count']}")

        except Exception as e:
            print(f"Error querying sensor counts: {e}")


if __name__ == "__main__":
    #query_yearly_transactions()
    #query_distinct_device_unit_count()
    #query_row_counts_and_error()
    query_distinct_sensor_counts()

