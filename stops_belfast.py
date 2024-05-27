import psycopg2
import json

def insert_into_database(sql_inserts):
    conn = psycopg2.connect(database="l3info_21", user="l3info_21", host="10.11.11.22", password="L3INFO_21")
    cursor = conn.cursor()

    for sql, params in sql_inserts:
        cursor.execute(sql, params)
    
    conn.commit()
    cursor.close()
    conn.close()

def de_geo_a_sql(geojson_data):
    features = geojson_data['features']
    sql_inserts = []
    
    for feature in features:
        route_type = feature['properties']['route_type']
        route_name = feature['properties']['route_name']
        route_I = feature['properties']['route_I']
        coordinates = feature['geometry']['coordinates']
        
        
        coordinates_json = json.dumps({'type': 'LineString', 'coordinates': coordinates})
        
        
        sql = "INSERT INTO stops_belfast (id, stop_I, name, ST_AsText(coordinates)) VALUES (DEFAULT, %s, %s, ST_AsText(ST_SetSRID(ST_MakePoint(%s, %s), 4326)))"

        
        
        sql_inserts.append((sql, (route_type, route_name, route_I, coordinates_json)))
    
    return sql_inserts

with open('routes.geojson') as file:
    geojson_data = json.load(file)
    sql_insert_statements = de_geo_a_sql(geojson_data)
    insert_into_database(sql_insert_statements)
