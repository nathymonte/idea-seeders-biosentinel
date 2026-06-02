erDiagram
    users ||--o{ environmental_reserves : owns
    environmental_reserves ||--o{ land_cover_analysis : has
    satellite_datasets ||--o{ land_cover_analysis : generates
    environmental_reserves ||--o{ alerts : triggers
    environmental_reserves ||--o{ iot_sensor_readings : receives

    users {
        int id PK
        string name
        string email
        string role
        timestamp created_at
    }

    environmental_reserves {
        int id PK
        int user_id FK
        string name
        string state
        string city
        numeric area_hectares
        geometry boundary
        timestamp created_at
    }

    satellite_datasets {
        int id PK
        string source
        int year
        int resolution_meters
        string file_path
        timestamp imported_at
    }

    land_cover_analysis {
        int id PK
        int reserve_id FK
        int dataset_id FK
        int class_code
        string class_name
        numeric area_hectares
        numeric percentage
        timestamp analyzed_at
    }

    alerts {
        int id PK
        int reserve_id FK
        string alert_type
        string severity
        string description
        timestamp detected_at
        string status
    }

    iot_sensor_readings {
        int id PK
        int reserve_id FK
        string sensor_type
        numeric value
        string unit
        timestamp measured_at
    }