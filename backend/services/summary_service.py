import json
from pathlib import Path

from sqlalchemy.orm import Session

from backend.repositories.reserve_repository import ReserveRepository
from backend.repositories.analysis_repository import AnalysisRepository


BASE_DIR = Path(__file__).resolve().parents[2]
GROUPS_PATH = BASE_DIR / "backend" / "resources" / "mapbiomas_groups.json"


class SummaryService:
    def __init__(self, db: Session):
        self.reserve_repository = ReserveRepository(db)
        self.analysis_repository = AnalysisRepository(db)
        self.groups = self._load_groups()

    def _load_groups(self):
        with open(GROUPS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_reserve_summary(self, reserve_id: int):
        reserve = self.reserve_repository.find_by_id(reserve_id)

        if reserve is None:
            raise ValueError(f"Reserva com id={reserve_id} não encontrada.")

        analysis = self.analysis_repository.find_by_reserve_id(reserve_id)

        if not analysis:
            raise ValueError(
                f"Nenhuma análise encontrada para a reserva id={reserve_id}."
            )

        dominant = max(analysis, key=lambda item: item.percentage)
        grouped_metrics = self._calculate_grouped_metrics(analysis)

        environmental_status = self._calculate_environmental_status(
            grouped_metrics
        )

        total_area_hectares = sum(float(item.area_hectares) for item in analysis)

        human_use_percentage = (
            grouped_metrics["urban_or_non_vegetated"]["percentage"]
            + grouped_metrics["agriculture_or_pasture"]["percentage"]
        )

        native_vegetation_percentage = grouped_metrics["native_vegetation"]["percentage"]

        return {
            "reserve_id": reserve.id,
            "reserve_name": reserve.name,
            "total_analyzed_area_hectares": round(total_area_hectares, 2),
            "number_of_detected_classes": len(analysis),
            "dominant_class": dominant.class_name,
            "dominant_percentage": float(dominant.percentage),
            "native_vegetation_percentage": native_vegetation_percentage,
            "human_use_percentage": round(human_use_percentage, 2),
            "groups": grouped_metrics,
            "environmental_status": environmental_status,
        }

    def _calculate_grouped_metrics(self, analysis):
        result = {}

        for group_key, group_data in self.groups.items():
            class_codes = group_data["classes"]
            label = group_data["label"]

            percentage_sum = sum(
                float(item.percentage)
                for item in analysis
                if item.class_code in class_codes
            )

            area_sum = sum(
                float(item.area_hectares)
                for item in analysis
                if item.class_code in class_codes
            )

            result[group_key] = {
                "label": label,
                "percentage": round(percentage_sum, 2),
                "area_hectares": round(area_sum, 2),
            }

        return result

    def _calculate_environmental_status(self, grouped_metrics):
        native = grouped_metrics["native_vegetation"]["percentage"]
        urban = grouped_metrics["urban_or_non_vegetated"]["percentage"]
        agriculture = grouped_metrics["agriculture_or_pasture"]["percentage"]

        human_use = urban + agriculture

        if native < 10 and human_use > 70:
            return "CRITICAL"

        if native < 30:
            return "WARNING"

        return "STABLE"