import csv
import psycopg2

conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()

with open('Paris_route_i_route_name.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file, delimiter=';')
    next(csv_reader) 

    for row in csv_reader:
        route_I, route_name, route_type = row

        cursor.execute("""
            INSERT INTO Paris_route_i_route_name (route_I, route_name, route_type)
            VALUES (%s, %s, %s);
        """, (route_I, route_name, route_type))

conn.commit()
cursor.close()
conn.close()