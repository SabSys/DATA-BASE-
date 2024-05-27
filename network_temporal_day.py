import csv
import psycopg2

conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()

with open('network_temporal_day.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)  

    for row in csv_reader:
        from_stop_I, to_stop_I, dep_time_ut, arr_time_ut, route_type, trip_I, seq, route_I = row

        cursor.execute("""
            INSERT INTO network_temporal_day_belfast(from_stop_I, to_stop_I, dep_time_ut, arr_time_ut, route_type, trip_I, seq, route_I)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (from_stop_I, to_stop_I, dep_time_ut, arr_time_ut, route_type, trip_I, seq, route_I))

conn.commit()
cursor.close()
conn.close()
