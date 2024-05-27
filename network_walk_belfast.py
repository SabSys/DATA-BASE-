import csv
import psycopg2

conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()

with open('temporal_walk_belfast.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)  # Skip header row

    for row in csv_reader:
        from_stop_I, to_stop_I, d, d_walk = row

        cursor.execute("""
            INSERT INTO temporal_walk_belfast (from_stop_I, to_stop_I, d, d_walk)
            VALUES (%s, %s, %s, %s);
        """, (from_stop_I, to_stop_I, d, d_walk))

conn.commit()
cursor.close()
conn.close()
