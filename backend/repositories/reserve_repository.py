from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database.models import EnvironmentalReserve


class ReserveRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(EnvironmentalReserve).all()

    def find_by_id(self, reserve_id: int):
        return (
            self.db.query(EnvironmentalReserve)
            .filter(EnvironmentalReserve.id == reserve_id)
            .first()
        )

    def update(self, reserve: EnvironmentalReserve):
        self.db.commit()
        self.db.refresh(reserve)
        return reserve

    def delete(self, reserve: EnvironmentalReserve):
        self.db.delete(reserve)
        self.db.commit()

    def find_all_with_geojson(self):
        return (
            self.db.query(
                EnvironmentalReserve.id,
                EnvironmentalReserve.name,
                EnvironmentalReserve.state,
                EnvironmentalReserve.city,
                EnvironmentalReserve.area_hectares,
                func.ST_AsGeoJSON(EnvironmentalReserve.boundary).label("boundary_geojson")
            )
            .all()
        )