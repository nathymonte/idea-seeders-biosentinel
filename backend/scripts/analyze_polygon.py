from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping, Polygon


BASE_DIR = Path(__file__).resolve().parents[2]
RASTER_PATH = BASE_DIR / "data" / "mapbiomas_2023.tif"

# Polígono pequeno de teste em EPSG:4326
# Coordenadas: longitude, latitude
TEST_POLYGON = Polygon([
    (-46.70, -23.60),
    (-46.69, -23.60),
    (-46.69, -23.59),
    (-46.70, -23.59),
    (-46.70, -23.60),
])

CLASS_NAMES = {
    3: "Formação Florestal",
    4: "Formação Savânica",
    5: "Mangue",
    6: "Floresta Alagável",
    11: "Campo Alagado e Área Pantanosa",
    12: "Formação Campestre",
    15: "Pastagem",
    19: "Lavoura Temporária",
    21: "Mosaico de Usos",
    24: "Área Urbanizada",
    25: "Outra Área Não Vegetada",
    30: "Mineração",
    33: "Rio, Lago e Oceano",
}


def main():
    if not RASTER_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {RASTER_PATH}")

    with rasterio.open(RASTER_PATH) as src:
        print("CRS do raster:", src.crs)
        print("Bounds do raster:", src.bounds)

        geometry = [mapping(TEST_POLYGON)]

        cropped_image, cropped_transform = mask(
            src,
            geometry,
            crop=True,
            filled=False
        )

        band = cropped_image[0]

        values, counts = np.unique(band.compressed(), return_counts=True)

        total_pixels = counts.sum()

        # Aproximação: MapBiomas 10m = 100 m² por pixel = 0.01 hectares
        pixel_area_hectares = 0.01

        print("\nResultado da análise do polígono:")
        print(f"Pixels válidos: {total_pixels}")

        for value, count in zip(values, counts):
            class_code = int(value)
            class_name = CLASS_NAMES.get(class_code, "Classe desconhecida")
            area_hectares = count * pixel_area_hectares
            percentage = (count / total_pixels) * 100

            print(
                f"Classe {class_code} - {class_name}: "
                f"{area_hectares:.2f} ha | {percentage:.2f}%"
            )


if __name__ == "__main__":
    main()