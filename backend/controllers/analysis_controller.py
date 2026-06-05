from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.repositories.analysis_repository import AnalysisRepository
from backend.services.mapbiomas_service import MapBiomasService
from backend.services.summary_service import SummaryService


router = APIRouter(
    prefix="/reserves",
    tags=["Analysis"]
)


@router.post("/{reserve_id}/analyze")
def analyze_reserve(
    reserve_id: int,
    dataset_id: int = 1,
    db: Session = Depends(get_db)
):
    try:
        service = MapBiomasService(db)

        results = service.analyze_reserve(
            reserve_id=reserve_id,
            dataset_id=dataset_id
        )

        return {
            "message": "Analysis completed successfully.",
            "reserve_id": reserve_id,
            "dataset_id": dataset_id,
            "results": results,
        }

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except FileNotFoundError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{reserve_id}/analysis")
def get_reserve_analysis(
    reserve_id: int,
    db: Session = Depends(get_db)
):
    repository = AnalysisRepository(db)
    analysis = repository.find_by_reserve_id(reserve_id)

    return [
        {
            "class_code": item.class_code,
            "class_name": item.class_name,
            "area_hectares": float(item.area_hectares),
            "percentage": float(item.percentage),
        }
        for item in analysis
    ]


@router.get("/{reserve_id}/summary")
def get_reserve_summary(
    reserve_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = SummaryService(db)
        return service.get_reserve_summary(reserve_id)

    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))