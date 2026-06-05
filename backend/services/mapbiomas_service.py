import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask
from geoalchemy2.shape import to_shape
from sqlalchemy.orm import Session

from backend.database.models import LandCoverAnalysis
from backend.repositories.reserve_repository import ReserveRepository
from backend.repositories.dataset_repository import DatasetRepository
from backend.repositories.analysis_repository import AnalysisRepository


BASE_DIR = Path(__file__).resolve().parents[2]
CLASSES_PATH = BASE_DIR / "backend" / "resources" / "mapbiomas_classes.json"


class MapBiomasService:
    def __init__(self, db: Session):
        self.db = db
        self.reserve_repository = ReserveRepository(db)
        self.dataset_repository = DatasetRepository(db)
        self.analysis_repository = AnalysisRepository(db)
        self.class_names = self._load_class_names()

    def _load_class_names(self):
        with open(CLASSES_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {int(key): value for key, value in data.items()}

    def analyze_reserve(self, reserve_id: int, dataset_id: int):
        reserve = self.reserve_repository.find_by_id(reserve_id)

        if reserve is None:
            raise ValueError(f"Reserva com id={reserve_id} não encontrada.")

        dataset = self.dataset_repository.find_by_id(dataset_id)

        if dataset is None:
            raise ValueError(f"Dataset com id={dataset_id} não encontrado.")

        raster_path = self._resolve_raster_path(dataset.file_path)
        geometry = to_shape(reserve.boundary)

        results = self._analyze_geometry(
            raster_path=raster_path,
            geometry=geometry
        )

        analyses = [
            LandCoverAnalysis(
                reserve_id=reserve_id,
                dataset_id=dataset_id,
                class_code=result["class_code"],
                class_name=result["class_name"],
                area_hectares=result["area_hectares"],
                percentage=result["percentage"],
            )
            for result in results
        ]

        self.analysis_repository.delete_by_reserve_and_dataset(
            reserve_id=reserve_id,
            dataset_id=dataset_id
        )

        self.analysis_repository.save_all(analyses)
        self.analysis_repository.commit()

        return results

    def _resolve_raster_path(self, file_path: str) -> Path:
        filename = Path(file_path).name
        local_path = BASE_DIR / "data" / filename

        if not local_path.exists():
            raise FileNotFoundError(f"GeoTIFF não encontrado: {local_path}")

        return local_path

    def _analyze_geometry(self, raster_path: Path, geometry):
        with rasterio.open(raster_path) as src:
            cropped_image, _ = mask(
                src,
                [geometry.__geo_interface__],
                crop=True,
                filled=False
            )

            band = cropped_image[0]
            values, counts = np.unique(band.compressed(), return_counts=True)

        total_pixels = counts.sum()

        if total_pixels == 0:
            raise ValueError("Nenhum pixel válido encontrado para o polígono.")

        pixel_area_hectares = 0.01
        results = []

        for value, count in zip(values, counts):
            class_code = int(value)
            class_name = self.class_names.get(class_code, "Classe desconhecida")
            area_hectares = round(float(count * pixel_area_hectares), 2)
            percentage = round(float((count / total_pixels) * 100), 2)

            results.append({
                "class_code": class_code,
                "class_name": class_name,
                "area_hectares": area_hectares,
                "percentage": percentage,
            })

        return results