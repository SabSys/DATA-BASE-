CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    route_type INTEGER,
    route_name VARCHAR(50),
    route_I INTEGER,
    coordinates GEOMETRY(LineString, 4326),
    latitude FLOAT,
    longitude FLOAT
);


