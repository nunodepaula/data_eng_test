CREATE TABLE IF NOT EXISTS data(
    timestamp TIMESTAMP PRIMARY KEY,
    wind_speed  REAL,
    power REAL,
    ambient_temperature REAL
);