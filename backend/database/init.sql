CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'ANALYST',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE environmental_reserves (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(150) NOT NULL,
    state CHAR(2) NOT NULL,
    city VARCHAR(120),
    area_hectares NUMERIC(12, 2),
    boundary GEOMETRY(POLYGON, 4326) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE satellite_datasets (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    resolution_meters INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE land_cover_analysis (
    id SERIAL PRIMARY KEY,
    reserve_id INTEGER NOT NULL REFERENCES environmental_reserves(id),
    dataset_id INTEGER NOT NULL REFERENCES satellite_datasets(id),
    class_code INTEGER NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    area_hectares NUMERIC(12, 2) NOT NULL,
    percentage NUMERIC(5, 2) NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    reserve_id INTEGER NOT NULL REFERENCES environmental_reserves(id),
    alert_type VARCHAR(80) NOT NULL,
    severity VARCHAR(30) NOT NULL,
    description TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'OPEN'
);

CREATE TABLE iot_sensor_readings (
    id SERIAL PRIMARY KEY,
    reserve_id INTEGER NOT NULL REFERENCES environmental_reserves(id),
    sensor_type VARCHAR(80) NOT NULL,
    value NUMERIC(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);