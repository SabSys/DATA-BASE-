CREATE TABLE network_combined (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT,
    route_type INTEGER
);

CREATE TABLE network_nodes (
    stop_I INTEGER PRIMARY KEY,
    lat FLOAT,
    lon FLOAT,
    name TEXT
);

CREATE TABLE network_rail (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_subway (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_temporal_day (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_temporal_week (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_tram (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_walk (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    d_walk INTEGER
);


--CREATE TABLE stops_test ( id SERIAL PRIMARY KEY, longitude FLOAT, latitude FLOAT, from_stop_I INTEGER, to_stop_I INTEGER, duration_avg FLOAT, route_type INTEGER, n_vehicles INTEGER);
--CREATE TABLE network_bus ( from_stop_I INTEGER, to_stop_I INTEGER, d INTEGER, duration_avg FLOAT, n_vehicles INTEGER, route_I_counts text);





