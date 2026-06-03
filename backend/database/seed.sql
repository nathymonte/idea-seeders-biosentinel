DELETE FROM land_cover_analysis;
DELETE FROM alerts;
DELETE FROM iot_sensor_readings;
DELETE FROM satellite_datasets;
DELETE FROM environmental_reserves;
DELETE FROM users;

ALTER SEQUENCE users_id_seq RESTART WITH 1;
ALTER SEQUENCE environmental_reserves_id_seq RESTART WITH 1;
ALTER SEQUENCE satellite_datasets_id_seq RESTART WITH 1;

INSERT INTO users (name, email, role)
VALUES ('Demo Admin', 'admin@biosentinel.com', 'ADMIN');

INSERT INTO environmental_reserves (
    user_id, name, state, city, area_hectares, boundary
)
VALUES (
    1,
    'Reserva Demo São Paulo',
    'SP',
    'São Paulo',
    123.21,
    ST_GeomFromText(
        'POLYGON((-46.70 -23.60, -46.69 -23.60, -46.69 -23.59, -46.70 -23.59, -46.70 -23.60))',
        4326
    )
);

INSERT INTO satellite_datasets (
    source, year, resolution_meters, file_path
)
VALUES (
    'MapBiomas Cobertura 10m',
    2023,
    10,
    '/data/mapbiomas_2023.tif'
);

INSERT INTO land_cover_analysis (
    reserve_id,
    dataset_id,
    class_code,
    class_name,
    area_hectares,
    percentage
)
VALUES
(1, 1, 24, 'Área Urbanizada', 108.19, 87.81),
(1, 1, 33, 'Rio, Lago e Oceano', 7.41, 6.01),
(1, 1, 21, 'Mosaico de Usos', 6.97, 5.66),
(1, 1, 25, 'Outra Área Não Vegetada', 0.48, 0.39),
(1, 1, 3, 'Formação Florestal', 0.09, 0.07),
(1, 1, 11, 'Campo Alagado e Área Pantanosa', 0.07, 0.06);