import json
import psycopg2


conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21") 
cursor = conn.cursor()

with open('sections.geojson', 'r') as file:
    geojson_data = json.load(file)


features = geojson_data['features']


for feature in features:
    geometry = feature['geometry']
    properties = feature['properties']
    from_stop_I = properties.get('from_stop_I')
    to_stop_I = properties.get('to_stop_I')
    duration_avg = properties.get('duration_avg')
    route_type = properties.get('route_type')
    n_vehicles = properties.get('n_vehicles')


    coordinates = geometry['coordinates']
    longitude, latitude = coordinates[0][0], coordinates[0][1]  


    cursor.execute("""
        INSERT INTO stops_test (longitude, latitude, from_stop_I, to_stop_I, duration_avg, route_type, n_vehicles)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (longitude, latitude, from_stop_I, to_stop_I, duration_avg, route_type, n_vehicles))


conn.commit()
cursor.close()
conn.close()
