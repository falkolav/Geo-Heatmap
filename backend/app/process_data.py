import os
import logging
import pandas as pd
import geopandas as gpd

from typing import Any
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from shapely.geometry import shape
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_csv_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def parse_geometry(geometry_str: str) -> shape:
    geometry_json = json.loads(geometry_str)
    return shape(geometry_json)


def transform_into_geometry_column(df: pd.DataFrame) -> pd.DataFrame:
    df["geometry"] = df["footprints_used"].apply(parse_geometry)
    df = df.drop(columns=["footprints_used"])
    return df


def convert_to_geodataframe(df: pd.DataFrame) -> gpd.GeoDataFrame:
    gdf = gpd.GeoDataFrame(df, geometry="geometry")
    gdf = gdf.set_crs(4326, allow_override=True)
    return gdf


def calculate_centroids(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    projected_gdf = gdf.to_crs("EPSG:3857")
    gdf["centroid"] = projected_gdf.centroid.to_crs(gdf.crs)
    return gdf


def save_to_database(
    gdf: gpd.GeoDataFrame, db_connection_string: str, table_name: str
) -> None:
    engine = create_engine(db_connection_string)
    gdf.to_postgis(table_name, engine, if_exists="replace", index=False)


def process_data(file_path: str, db_connection_string: str, table_name: str) -> None:
    raw_usage_df = read_csv_data(file_path)
    transformed_usage_df = transform_into_geometry_column(raw_usage_df)
    usage_gdf = convert_to_geodataframe(transformed_usage_df)
    centroids_gdf = calculate_centroids(usage_gdf)
    save_to_database(centroids_gdf, db_connection_string, table_name)


if __name__ == "__main__":

    file_path = "./data/data.csv"
    db_connection_string = (
        f"postgresql://geo_heatmap_user:G30_H34TmAp_4pp!@db:5432/geo_heatmap_db"
    )
    table_name = "usage"
    try:
        process_data(file_path, db_connection_string, table_name)
        logger.info("Data processing successful!")
    except Exception as e:
        logger.info(f"Error saving: {e}")
