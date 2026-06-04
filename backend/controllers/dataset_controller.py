from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from backend.database.connection import get_db
from backend.database.models import SatelliteDataset


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

class DatasetUpdateRequest(BaseModel):
    source: Optional[str] = None
    year: Optional[int] = None
    resolution_meters: Optional[int] = None
    file_path: Optional[str] = None

@router.put("/{dataset_id}")
def update_dataset(
    dataset_id: int,
    request: DatasetUpdateRequest,
    db: Session = Depends(get_db)
):
    dataset = (
        db.query(SatelliteDataset)
        .filter(SatelliteDataset.id == dataset_id)
        .first()
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset com id={dataset_id} não encontrado."
        )

    if request.source is not None:
        dataset.source = request.source

    if request.year is not None:
        dataset.year = request.year

    if request.resolution_meters is not None:
        dataset.resolution_meters = request.resolution_meters

    if request.file_path is not None:
        dataset.file_path = request.file_path

    db.commit()
    db.refresh(dataset)

    return {
        "message": "Dataset updated successfully.",
        "dataset": {
            "id": dataset.id,
            "source": dataset.source,
            "year": dataset.year,
            "resolution_meters": dataset.resolution_meters,
            "file_path": dataset.file_path,
        }
    }


@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    dataset = (
        db.query(SatelliteDataset)
        .filter(SatelliteDataset.id == dataset_id)
        .first()
    )

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset com id={dataset_id} não encontrado."
        )

    db.delete(dataset)
    db.commit()

    return {
        "message": "Dataset deleted successfully.",
        "dataset_id": dataset_id
    }