from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import json

from backend.database.connection import get_db
from backend.repositories.reserve_repository import ReserveRepository


router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)


class ReserveUpdateRequest(BaseModel):
    name: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    area_hectares: Optional[float] = None


@router.get("")
def list_reserves(db: Session = Depends(get_db)):
    repository = ReserveRepository(db)
    reserves = repository.find_all_with_geojson()

    return [
        {
            "id": reserve.id,
            "name": reserve.name,
            "state": reserve.state,
            "city": reserve.city,
            "area_hectares": float(reserve.area_hectares),
            "boundary": json.loads(reserve.boundary_geojson),
        }
        for reserve in reserves
    ]


@router.put("/{reserve_id}")
def update_reserve(
    reserve_id: int,
    request: ReserveUpdateRequest,
    db: Session = Depends(get_db)
):
    repository = ReserveRepository(db)
    reserve = repository.find_by_id(reserve_id)

    if reserve is None:
        raise HTTPException(
            status_code=404,
            detail=f"Reserva com id={reserve_id} não encontrada."
        )

    if request.name is not None:
        reserve.name = request.name

    if request.state is not None:
        reserve.state = request.state

    if request.city is not None:
        reserve.city = request.city

    if request.area_hectares is not None:
        reserve.area_hectares = request.area_hectares

    reserve = repository.update(reserve)

    return {
        "message": "Reserve updated successfully.",
        "reserve": {
            "id": reserve.id,
            "name": reserve.name,
            "state": reserve.state,
            "city": reserve.city,
            "area_hectares": float(reserve.area_hectares),
        }
    }


@router.delete("/{reserve_id}")
def delete_reserve(
    reserve_id: int,
    db: Session = Depends(get_db)
):
    repository = ReserveRepository(db)
    reserve = repository.find_by_id(reserve_id)

    if reserve is None:
        raise HTTPException(
            status_code=404,
            detail=f"Reserva com id={reserve_id} não encontrada."
        )

    repository.delete(reserve)

    return {
        "message": "Reserve deleted successfully.",
        "reserve_id": reserve_id
    }