import os
import tempfile

import pandas as pd
import geopandas as gpd
import psycopg2
from sqlalchemy import create_engine
from shapely.geometry import shape

from app.utils import (
    read_csv_data,
    parse_geometry,
    transform_into_geometry_column,
    convert_to_geodataframe,
    calculate_centroids,
    save_to_database,
    process_data,
)


def test_read_csv_data():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv") as f:
        f.write("col1,col2\n1,2\n3,4\n")
        f.flush()

        result = read_csv_data(f.name)

        assert isinstance(result, pd.DataFrame)
        assert result.equals(pd.DataFrame({"col1": [1, 3], "col2": [2, 4]}))


def test_parse_geometry():
    geometry_str = '{"type":"Polygon","coordinates":[[[1,2],[2,3],[3,4],[4,1],[1,2]]]}'

    result = parse_geometry(geometry_str)

    assert result.geom_type == "Polygon"


def test_transform_into_geometry_column():
    df = pd.DataFrame(
        {
            "footprints_used": [
                '{"type":"Polygon","coordinates":[[[1,2],[2,3],[3,4],[4,1],[1,2]]]}',
                '{"type":"Polygon","coordinates":[[[5,6],[6,7],[7,8],[8,5],[5,6]]]}',
            ]
        }
    )

    result = transform_into_geometry_column(df)

    assert "geometry" in result.columns


def test_convert_to_geodataframe():
    df = pd.DataFrame(
        {
            "footprints_used": [
                '{"type":"Polygon","coordinates":[[[1,2],[2,3],[3,4],[4,1],[1,2]]]}',
                '{"type":"Polygon","coordinates":[[[5,6],[6,7],[7,8],[8,5],[5,6]]]}',
            ]
        }
    )
    df = transform_into_geometry_column(df)

    result = convert_to_geodataframe(df)

    assert isinstance(result, gpd.GeoDataFrame)
