# atl-zipcodes

A small Python script that renders a map of selected Atlanta-area ZIP codes,
color-coded and labeled with neighborhood names, over an OpenStreetMap
basemap.

![Sample output](atlanta_zip_map.png)

## ZIP codes covered

| ZIP   | Area                          |
| ----- | ----------------------------- |
| 30022 | Alpharetta / Johns Creek      |
| 30024 | Suwanee                       |
| 30067 | Marietta (Powers Ferry)       |
| 30068 | Marietta (East Cobb)          |
| 30071 | Norcross                      |
| 30092 | Peachtree Corners             |
| 30096 | Duluth                        |
| 30305 | Buckhead                      |
| 30318 | West Midtown / Westside       |
| 30324 | NE Atlanta                    |
| 30328 | Sandy Springs                 |
| 30338 | Dunwoody                      |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python zipcodes.py
```

On first run the script downloads the TIGER/Line 2022 ZCTA shapefile
(~520 MB) into the working directory and extracts it. Subsequent runs reuse
the local copy. The map is written to `atlanta_zip_map.png`.

To change which ZIPs are rendered, edit the `ZIP_LABELS` dict at the top of
`zipcodes.py`.

## Data source

ZIP Code Tabulation Areas from the U.S. Census Bureau's TIGER/Line 2022
release: <https://www2.census.gov/geo/tiger/TIGER2022/ZCTA520/>. Basemap
tiles &copy; OpenStreetMap contributors.
