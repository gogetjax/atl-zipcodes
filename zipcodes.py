"""Render an Atlanta-area ZIP code map with labels and color-coding.

Reads ZCTA polygons from the TIGER/Line shapefile, filters to the configured
ZIPs, and overlays them on an OpenStreetMap basemap. The shapefile is
downloaded automatically on first run if not present.
"""

from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt

ZCTA_URL = "https://www2.census.gov/geo/tiger/TIGER2022/ZCTA520/tl_2022_us_zcta520.zip"
ZCTA_SHP = Path("tl_2022_us_zcta520.shp")
OUTPUT_PNG = Path("atlanta_zip_map.png")

# ZIP -> neighborhood label
ZIP_LABELS = {
    "30068": "Marietta (East Cobb)",
    "30067": "Marietta (Powers Ferry)",
    "30092": "Peachtree Corners",
    "30071": "Norcross",
    "30328": "Sandy Springs",
    "30338": "Dunwoody",
    "30096": "Duluth",
    "30022": "Alpharetta / Johns Creek",
    "30024": "Suwanee",
    "30324": "NE Atlanta",
    "30318": "West Midtown / Westside",
    "30305": "Buckhead",
}


def ensure_shapefile() -> None:
    """Download and unzip the TIGER/Line ZCTA shapefile if missing."""
    if ZCTA_SHP.exists():
        return
    archive = Path(ZCTA_URL.split("/")[-1])
    print(f"Downloading {ZCTA_URL} ...")
    urlretrieve(ZCTA_URL, archive)
    print("Extracting...")
    with ZipFile(archive) as zf:
        zf.extractall(".")
    archive.unlink()


def main() -> None:
    ensure_shapefile()

    zctas = gpd.read_file(ZCTA_SHP)
    atl = zctas[zctas["ZCTA5CE20"].isin(ZIP_LABELS)].to_crs(epsg=3857)

    ax = atl.plot(
        column="ZCTA5CE20",
        cmap="tab20",
        edgecolor="black",
        linewidth=0.5,
        figsize=(10, 10),
        alpha=0.6,
    )
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

    for _, row in atl.iterrows():
        pt = row.geometry.representative_point()
        label = f"{row['ZCTA5CE20']} – {ZIP_LABELS[row['ZCTA5CE20']]}"
        plt.text(pt.x, pt.y, label, fontsize=6, ha="center")

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)
    print(f"Wrote {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
