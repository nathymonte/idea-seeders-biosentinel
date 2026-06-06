SET client_encoding = 'UTF8';

INSERT INTO users (name, email, password_hash, role)
VALUES (
    'Demo Admin',
    'admin@biosentinel.com',
    '$2b$12$NJ/rV8pujpx0eS1Xaf/5DO.mOatq2bMO1BMcDsefmtozbs6EMZ3O6',
    'ADMIN'
);

INSERT INTO environmental_reserves (
    user_id, name, state, city, area_hectares, boundary
)
VALUES (
    1,
    'Reserva Cantareira Demo',
    'SP',
    'São Paulo',
    497.29,
    ST_GeomFromText(
        'POLYGON((
            -46.66 -23.43,
            -46.62 -23.43,
            -46.62 -23.39,
            -46.66 -23.39,
            -46.66 -23.43
        ))',
        4326
    )
);

INSERT INTO environmental_reserves (
    user_id,
    name,
    state,
    city,
    area_hectares,
    boundary
)
VALUES (
    1,
    'Reserva Amazônia Demo',
    'AM',
    'Manaus',
    400.00,
    ST_GeomFromText(
        'POLYGON((
            -60.35 -2.05,
            -60.33 -2.05,
            -60.33 -2.03,
            -60.35 -2.03,
            -60.35 -2.05
        ))',
        4326
    )
);

INSERT INTO environmental_reserves (
    user_id,
    name,
    state,
    city,
    area_hectares,
    boundary
)
VALUES (
    1,
    'Reserva Pantanal Demo',
    'MS',
    'Corumbá',
    400.00,
    ST_GeomFromText(
        'POLYGON((
        -57.65 -19.00,
        -57.63 -19.00,
        -57.63 -18.98,
        -57.65 -18.98,
        -57.65 -19.00
        ))',
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
(1, 1, 3,  'Formação Florestal', 1509.01, 75.86),
(1, 1, 21, 'Mosaico de Usos', 237.09, 11.92),
(1, 1, 24, 'Área Urbanizada', 204.98, 10.30),
(1, 1, 9,  'Classe desconhecida', 17.93, 0.90),
(1, 1, 15, 'Pastagem', 11.99, 0.60),
(1, 1, 33, 'Rio, Lago e Oceano', 7.53, 0.38),
(1, 1, 11, 'Campo Alagado e Área Pantanosa', 0.50, 0.03),
(1, 1, 19, 'Lavoura Temporária', 0.11, 0.01),
(1, 1, 12, 'Formação Campestre', 0.02, 0.00),
(2, 1, 3,  'Formação Florestal', 458.76, 92.67),
(2, 1, 11, 'Campo Alagado e Área Pantanosa', 6.98, 1.41),
(2, 1, 21, 'Mosaico de Usos', 29.19, 5.90),
(2, 1, 24, 'Área Urbanizada', 0.08, 0.02),
(2, 1, 25, 'Outra Área Não Vegetada', 0.05, 0.01),
(3, 1, 11, 'Campo Alagado e Área Pantanosa', 188.68, 37.94),
(3, 1, 3,  'Formação Florestal', 295.50, 59.42),
(3, 1, 21, 'Mosaico de Usos', 0.29, 0.06),
(3, 1, 24, 'Área Urbanizada', 93.68, 18.84),
(3, 1, 25, 'Outra Área Não Vegetada', 0.48, 0.09),
(3, 1, 33, 'Rio, Lago e Oceano', 107.34, 21.58),
(3, 1, 12, 'Formação Campestre', 0.12, 0.02);