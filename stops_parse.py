import psycopg2
import json


conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
cursor = conn.cursor()
 


create_table_query = '''
CREATE TABLE stops (
    id SERIAL PRIMARY KEY,
    stop_id VARCHAR,
    name VARCHAR,
    coordinates POINT
);
'''


cursor.execute(create_table_query)
conn.commit()


with open('stops.geojson', 'r') as file:
    data = json.load(file)


for feature in data['features']:
    stop_id = feature['properties']['stop_I']
    name = feature['properties']['name']
    coordinates = feature['geometry']['coordinates']

    
    insert_query = '''
    INSERT INTO stops (stop_id, name, coordinates)
    VALUES (%s, %s, POINT(%s, %s));
    '''

    
    cursor.execute(insert_query, (stop_id, name, coordinates[0], coordinates[1]))


conn.commit()


cursor.close()
conn.close()

