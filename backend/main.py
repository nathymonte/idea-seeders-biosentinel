from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.models import EnvironmentalReserve, SatelliteDataset, LandCoverAnalysis


app = FastAPI(
    title="BioSentinel API",
    description="API for environmental reserve monitoring using satellite data.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "BioSentinel API running"}


@app.get("/reserves")
def list_reserves(db: Session = Depends(get_db)):
    reserves = db.query(EnvironmentalReserve).all()

    return [
        {
            "id": reserve.id,
            "name": reserve.name,
            "state": reserve.state,
            "city": reserve.city,
            "area_hectares": float(reserve.area_hectares),
        }
        for reserve in reserves
    ]


@app.get("/datasets")
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(SatelliteDataset).all()

    return [
        {
            "id": dataset.id,
            "source": dataset.source,
            "year": dataset.year,
            "resolution_meters": dataset.resolution_meters,
            "file_path": dataset.file_path,
        }
        for dataset in datasets
    ]


@app.get("/reserves/{reserve_id}/analysis")
def get_reserve_analysis(
    reserve_id: int,
    db: Session = Depends(get_db)
):
    analysis = (
        db.query(LandCoverAnalysis)
        .filter(LandCoverAnalysis.reserve_id == reserve_id)
        .order_by(LandCoverAnalysis.percentage.desc())
        .all()
    )

    return [
        {
            "class_code": item.class_code,
            "class_name": item.class_name,
            "area_hectares": float(item.area_hectares),
            "percentage": float(item.percentage),
        }
        for item in analysis
    ]