from types import SimpleNamespace

from backend.services.summary_service import SummaryService


def test_calculate_environmental_status_critical():
    service = SummaryService.__new__(SummaryService)

    grouped_percentages = {
        "native_vegetation": {"percentage": 0.2},
        "urban_or_non_vegetated": {"percentage": 88.2},
        "agriculture_or_pasture": {"percentage": 5.66},
    }

    result = service._calculate_environmental_status(grouped_percentages)

    assert result == "CRITICAL"


def test_calculate_grouped_percentages():
    service = SummaryService.__new__(SummaryService)

    service.groups = {
        "native_vegetation": {
            "label": "Vegetação Nativa",
            "classes": [3, 4, 5, 6, 11, 12],
        },
        "urban_or_non_vegetated": {
            "label": "Área Urbana ou Não Vegetada",
            "classes": [24, 25, 30],
        },
    }

    analysis = [
        SimpleNamespace(class_code=3, percentage=10.0),
        SimpleNamespace(class_code=11, percentage=5.0),
        SimpleNamespace(class_code=24, percentage=80.0),
        SimpleNamespace(class_code=25, percentage=5.0),
    ]

    result = service._calculate_grouped_metrics(analysis)

    assert result["native_vegetation"]["percentage"] == 15.0
    assert result["urban_or_non_vegetated"]["percentage"] == 85.0