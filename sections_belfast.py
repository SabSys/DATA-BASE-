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

def de_geojson_to_sql(geojson_data):
    features = geojson_data['features']
    sql_inserts = []
    
    for feature in features:
        from_stop_I = str(feature['properties']['from_stop_I'])
        to_stop_I = str(feature['properties']['to_stop_I'])
        n_vehicles = int(feature['properties']['n_vehicles'])
        route_type = int(feature['properties']['route_type'])
        duration_avg = float(feature['properties']['duration_avg'])
        
        
        coordinates = feature['geometry']['coordinates']
        coordinates_str = ','.join([f'{x} {y}' for x, y in coordinates])
        linestring = f"LINESTRING({coordinates_str})"
        
        route_I_counts = json.dumps(feature['properties']['route_I_counts'])
        
        
        sql = f"INSERT INTO sections_belfast (from_stop_I, to_stop_I, n_vehicles, route_type, duration_avg, route_I_counts, coordinates) VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326))"
        
        
        sql_inserts.append((sql, (from_stop_I, to_stop_I, n_vehicles, route_type, duration_avg, route_I_counts, linestring)))
    
    return sql_inserts

with open('sections.geojson') as file:
    geojson_data = json.load(file)
    sql_insert_statements = de_geojson_to_sql(geojson_data)
    insert_into_database(sql_insert_statements)
