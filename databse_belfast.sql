CREATE TABLE network_combined_fast (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT,
    route_type INTEGER
);

CREATE TABLE network_nodes_belfast (
    stop_I INTEGER PRIMARY KEY,
    lat FLOAT,
    lon FLOAT,
    name TEXT
);



CREATE TABLE network_temporal_day_belfast (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_temporal_week_belfast (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);



CREATE TABLE network_walk_belfast (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    d_walk INTEGER
);

CREATE TABLE  routes_belfast (
    route_I INT PRIMARY KEY,
    route_name VARCHAR(50),
    route_type INT,
    geometry JSONB);

CREATE TABLE stops_belfast (
    id SERIAL PRIMARY KEY,
    stop_I TEXT,
    name TEXT,
    coordinates GEOMETRY(Point, 4326)
);

CREATE TABLE sections_belfast (
    id SERIAL PRIMARY KEY,
    from_stop_I TEXT,
    to_stop_I TEXT,
    n_vehicles INTEGER,
    route_type INTEGER,
    duration_avg FLOAT,
    route_I_counts JSONB,
    coordinates text,
);
CREATE TABLE network_bus_belfast (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE routes_beta_belfast (
    from_stop_i INTEGER,
    to_stop_i INTEGER,
    route_i INTEGER
);

CREATE TABLE routes_alpha_belfast (
    from_stop_i INTEGER,
    to_stop_i INTEGER,
    route_i INTEGER
);


INSERT INTO routes_alpha_belfast (from_stop_i, to_stop_i, route_i)
SELECT from_stop_i, to_stop_i, route_i
FROM routes_beta_belfast
UNION ALL
SELECT to_stop_i, from_stop_i, route_i
FROM routes_beta_belfast;


INSERT INTO routes_beta_belfast (from_stop_i, to_stop_i, route_i)
SELECT from_stop_i, to_stop_i, 
    CAST(SPLIT_PART(route_pair, ':', 1) AS INTEGER) AS route_i
FROM (
    SELECT from_stop_i, to_stop_i, 
        regexp_split_to_table(route_I_counts, ',') AS route_pair
    FROM network_bus_belfast
) AS split_pairs;


CREATE TABLE routes_bus_belfast AS
SELECT from_stop_i AS stop_i, route_i
FROM routes_alpha_belfast

UNION ALL

SELECT to_stop_i AS stop_i, route_i
FROM routes_alpha_belfast;



CREATE TABLE network_nodes_with_routes AS
SELECT 
    stops.stop_i,
    stops.lat,
    stops.lon,
    stops.name,
    routes.route_i 
FROM 
    network_nodes_belfast stops
JOIN 
    routes_bus_belfast routes
ON 
    stops.stop_i = routes.stop_i;



