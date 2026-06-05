from sqlalchemy.orm import Session

from backend.database.models import LandCoverAnalysis


class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_reserve_id(self, reserve_id: int):
        return (
            self.db.query(LandCoverAnalysis)
            .filter(LandCoverAnalysis.reserve_id == reserve_id)
            .order_by(LandCoverAnalysis.percentage.desc())
            .all()
        )

    def delete_by_reserve_and_dataset(self, reserve_id: int, dataset_id: int):
        (
            self.db.query(LandCoverAnalysis)
            .filter(
                LandCoverAnalysis.reserve_id == reserve_id,
                LandCoverAnalysis.dataset_id == dataset_id,
            )
            .delete()
        )

    def save_all(self, analyses: list[LandCoverAnalysis]):
        for analysis in analyses:
            self.db.add(analysis)

    def commit(self):
        self.db.commit()