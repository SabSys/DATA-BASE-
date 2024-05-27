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
        
        
        coordinates_str = ', '.join([f'{coord[0]} {coord[1]}' for coord in coordinates])
        
        
        sql = f"INSERT INTO routes (route_type, route_name, route_I, coordinates) VALUES (%s, %s, %s, ST_GeomFromText('LINESTRING({coordinates_str})', 4326)::geography)"
        
        
        sql_inserts.append((sql, (route_type, route_name, route_I)))
    
    return sql_inserts

with open('routes.geojson') as file:
    geojson_data = json.load(file)
    sql_insert_statements = de_geo_a_sql(geojson_data)
    insert_into_database(sql_insert_statements)
