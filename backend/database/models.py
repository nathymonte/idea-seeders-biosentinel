from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from backend.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), nullable=False, default="ANALYST")
    created_at = Column(DateTime, server_default=func.now())


class EnvironmentalReserve(Base):
    __tablename__ = "environmental_reserves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(150), nullable=False)
    state = Column(String(2), nullable=False)
    city = Column(String(120))
    area_hectares = Column(Numeric(12, 2))
    boundary = Column(Geometry("POLYGON", srid=4326), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class SatelliteDataset(Base):
    __tablename__ = "satellite_datasets"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    resolution_meters = Column(Integer, nullable=False)
    file_path = Column(Text, nullable=False)
    imported_at = Column(DateTime, server_default=func.now())


class LandCoverAnalysis(Base):
    __tablename__ = "land_cover_analysis"

    id = Column(Integer, primary_key=True, index=True)
    reserve_id = Column(Integer, ForeignKey("environmental_reserves.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("satellite_datasets.id"), nullable=False)
    class_code = Column(Integer, nullable=False)
    class_name = Column(String(100), nullable=False)
    area_hectares = Column(Numeric(12, 2), nullable=False)
    percentage = Column(Numeric(5, 2), nullable=False)
    analyzed_at = Column(DateTime, server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    reserve_id = Column(Integer, ForeignKey("environmental_reserves.id"), nullable=False)
    alert_type = Column(String(80), nullable=False)
    severity = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    detected_at = Column(DateTime, server_default=func.now())
    status = Column(String(30), default="OPEN")


class IoTSensorReading(Base):
    __tablename__ = "iot_sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    reserve_id = Column(Integer, ForeignKey("environmental_reserves.id"), nullable=False)
    sensor_type = Column(String(80), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), nullable=False)
    measured_at = Column(DateTime, server_default=func.now())