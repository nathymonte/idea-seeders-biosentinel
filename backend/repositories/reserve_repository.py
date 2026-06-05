from sqlalchemy.orm import Session

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