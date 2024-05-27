import csv
import psycopg2

conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()

with open('network_nodes.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader)  

    for row in csv_reader:
        stop_I, lat, lon, name = row

        cursor.execute("""
            INSERT INTO network_nodes_belfast (stop_I, lat, lon, name)
            VALUES (%s, %s, %s, %s);
        """, (stop_I, lat, lon, name))

conn.commit()
cursor.close()
conn.close()
