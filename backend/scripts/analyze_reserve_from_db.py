from pathlib import Path

import numpy as np
import psycopg2
import rasterio
from rasterio.mask import mask
from shapely import wkb
import json


BASE_DIR = Path(__file__).resolve().parents[2]
RASTER_PATH = BASE_DIR / "data" / "mapbiomas_2023.tif"

DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "biosentinel",
    "user": "biosentinel",
    "password": "biosentinel",
}

RESERVE_ID = 1
DATASET_ID = 1

CLASSES_PATH = BASE_DIR / "backend" / "resources" / "mapbiomas_classes.json"


def load_class_names():
    with open(CLASSES_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return {int(key): value for key, value in data.items()}

def get_reserve_boundary(connection, reserve_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                id,
                name,
                ST_AsEWKB(boundary) AS boundary_wkb
            FROM environmental_reserves
            WHERE id = %s;
            """,
            (reserve_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise ValueError(f"Reserva com id={reserve_id} não encontrada.")

        reserve_id, reserve_name, boundary_wkb = result

        geometry = wkb.loads(bytes(boundary_wkb))

        return {
            "id": reserve_id,
            "name": reserve_name,
            "geometry": geometry,
        }


def clear_previous_analysis(connection, reserve_id, dataset_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM land_cover_analysis
            WHERE reserve_id = %s
              AND dataset_id = %s;
            """,
            (reserve_id, dataset_id)
        )


def save_analysis_result(
    connection,
    reserve_id,
    dataset_id,
    class_code,
    class_name,
    area_hectares,
    percentage,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO land_cover_analysis (
                reserve_id,
                dataset_id,
                class_code,
                class_name,
                area_hectares,
                percentage
            )
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (
                reserve_id,
                dataset_id,
                class_code,
                class_name,
                area_hectares,
                percentage,
            )
        )


def analyze_geometry(geometry, class_names):
    with rasterio.open(RASTER_PATH) as src:
        print("CRS do raster:", src.crs)
        print("Bounds do raster:", src.bounds)

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
            class_name = class_names.get(class_code, "Classe desconhecida")
            area_hectares = round(float(count * pixel_area_hectares), 2)
            percentage = round(float((count / total_pixels) * 100), 2)

            results.append({
                "class_code": class_code,
                "class_name": class_name,
                "area_hectares": area_hectares,
                "percentage": percentage,
            })

        return results


def main():
    if not RASTER_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {RASTER_PATH}")

    connection = psycopg2.connect(**DATABASE_CONFIG)

    try:
        reserve = get_reserve_boundary(connection, RESERVE_ID)
        class_names = load_class_names()

        print(f"Reserva encontrada: {reserve['name']}")

        results = analyze_geometry(reserve["geometry"], class_names)

        clear_previous_analysis(connection, RESERVE_ID, DATASET_ID)

        print("\nResultado calculado:")

        for result in results:
            print(
                f"Classe {result['class_code']} - {result['class_name']}: "
                f"{result['area_hectares']} ha | "
                f"{result['percentage']}%"
            )

            save_analysis_result(
                connection=connection,
                reserve_id=RESERVE_ID,
                dataset_id=DATASET_ID,
                class_code=result["class_code"],
                class_name=result["class_name"],
                area_hectares=result["area_hectares"],
                percentage=result["percentage"],
            )

        connection.commit()

        print("\nAnálise salva em land_cover_analysis.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()