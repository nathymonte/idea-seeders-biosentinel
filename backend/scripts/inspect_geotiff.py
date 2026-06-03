from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import Window


BASE_DIR = Path(__file__).resolve().parents[2]
RASTER_PATH = BASE_DIR / "data" / "mapbiomas_2023.tif"


def print_basic_metadata(src):
    print("Arquivo:", RASTER_PATH)
    print("Driver:", src.driver)
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Width:", src.width)
    print("Height:", src.height)
    print("Count bands:", src.count)
    print("Resolution:", src.res)
    print("Dtype:", src.dtypes)
    print("NoData:", src.nodata)


def inspect_sample_window(src, window_size=2000):
    center_col = src.width // 2
    center_row = src.height // 2

    col_off = max(center_col - window_size // 2, 0)
    row_off = max(center_row - window_size // 2, 0)

    window = Window(
        col_off=col_off,
        row_off=row_off,
        width=window_size,
        height=window_size
    )

    band = src.read(1, window=window, masked=True)

    values, counts = np.unique(band.compressed(), return_counts=True)

    print(f"\nAmostra analisada: {window_size} x {window_size} pixels")
    print("Classes encontradas na amostra:")

    for value, count in zip(values, counts):
        print(f"Classe {int(value)}: {count} pixels")


def main():
    if not RASTER_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {RASTER_PATH}")

    with rasterio.open(RASTER_PATH) as src:
        print_basic_metadata(src)
        inspect_sample_window(src)


if __name__ == "__main__":
    main()