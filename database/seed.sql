INSERT INTO users (name, email, role)
VALUES ('Nath', 'nath@email.com', 'ADMIN');

INSERT INTO environmental_reserves (
    user_id, name, state, city, area_hectares, boundary
)
VALUES (
    1,
    'Reserva Demo',
    'SP',
    'São Paulo',
    120.50,
    ST_GeomFromText(
        'POLYGON((-46.70 -23.60, -46.69 -23.60, -46.69 -23.59, -46.70 -23.59, -46.70 -23.60))',
        4674
    )
);

INSERT INTO satellite_datasets (source, year, resolution_meters, file_path)
VALUES ('MapBiomas Cobertura 10m', 2023, 10, '/data/mapbiomas_2023.tif');

INSERT INTO land_cover_analysis (
    reserve_id, dataset_id, class_code, class_name, area_hectares, percentage
)
VALUES
(1, 1, 3, 'Formação Florestal', 90.00, 74.69),
(1, 1, 15, 'Pastagem', 25.00, 20.75),
(1, 1, 24, 'Área Urbana', 5.50, 4.56);

INSERT INTO alerts (
    reserve_id, alert_type, severity, description
)
VALUES (
    1,
    'VEGETATION_LOSS',
    'HIGH',
    'Possível redução de cobertura vegetal detectada na reserva.'
);

INSERT INTO iot_sensor_readings (
    reserve_id, sensor_type, value, unit
)
VALUES
(1, 'TEMPERATURE', 32.5, 'C'),
(1, 'HUMIDITY', 41.2, '%'),
(1, 'SMOKE_LEVEL', 12.8, 'ppm');