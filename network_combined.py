import csv
import psycopg2

conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()

with open('network_combined.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)  

    for row in csv_reader:
        from_stop_I, to_stop_I, d, duration_avg, n_vehicles, route_I_counts, route_type = row

        cursor.execute("""
            INSERT INTO network_combined_fast (from_stop_I, to_stop_I, d, duration_avg, n_vehicles, route_I_counts, route_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (from_stop_I, to_stop_I, d, duration_avg, n_vehicles, route_I_counts, route_type))

conn.commit()
cursor.close()
conn.close()
