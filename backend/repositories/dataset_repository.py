from sqlalchemy.orm import Session

from backend.database.models import SatelliteDataset


class DatasetRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(SatelliteDataset).all()

    def find_by_id(self, dataset_id: int):
        return (
            self.db.query(SatelliteDataset)
            .filter(SatelliteDataset.id == dataset_id)
            .first()
        )

    def update(self, dataset: SatelliteDataset):
        self.db.commit()
        self.db.refresh(dataset)
        return dataset

    def delete(self, dataset: SatelliteDataset):
        self.db.delete(dataset)
        self.db.commit()