from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Tuple
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import psycopg2
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class PointData(BaseModel):
    lat: float
    lng: float
    weight: int


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

load_dotenv()

db_username = "geo_heatmap_user"
db_password = "G30_H34TmAp_4pp!"
db_name = "geo_heatmap_db"


def fetch_usage_data(org_id: str) -> List[Tuple[float, float]]:
    """
    Fetches the usage data for a given organization ID.

    Args:
        org_id (str): A string representing the organization ID for which to fetch usage data.

    Returns:
        List[Tuple[float, float]]: A list of tuples representing the latitude, longitude, and weight (i.e., usage count)
        of each usage data point.
    """
    logger.info(f"Fetching usage data for organization ID {org_id}")

    conn = psycopg2.connect(
        host="db", database=db_name, user=db_username, password=db_password
    )
    logger.info("Connected to database")

    cursor = conn.cursor()

    if org_id == "all":
        query = "SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM usage GROUP BY centroid;"
    else:
        query = f"SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM usage WHERE org_id = {org_id} GROUP BY centroid;"

    logger.debug(f"Executing query: {query}")
    cursor.execute(query)

    data = cursor.fetchall()

    logger.info(f"Fetched {len(data)} rows of usage data from database")
    conn.close()

    return data


@app.get("/heatmap-data/{org_id}", response_model=List[PointData])
def get_heatmap_data(org_id: str):
    """
    Endpoint that returns the usage data for a given organization ID in the format required by the frontend.

    Args:
        org_id (str): A string representing the organization ID for which to fetch usage data.

    Returns:
        List[PointData]: A list of PointData objects, where each object represents a usage data point with the
        latitude, longitude, and weight (i.e., usage count) specified.
    """

    logger.info(f"Received request for heatmap data for org ID {org_id}")

    start_time = time.monotonic()

    data = fetch_usage_data(org_id)
    point_data = [
        PointData(lat=lat, lng=lng, weight=weight) for lat, lng, weight in data
    ]

    response_time = time.monotonic() - start_time

    if not point_data:
        raise HTTPException(status_code=204, detail="No data available")
        logger.warning(f"No data available for org ID {org_id}")
        return []

    logger.info(
        f"Returning heatmap data for org ID {org_id} ({len(point_data)} points) in {response_time:.2f}s"
    )

    return point_data


def fetch_org_ids() -> List[int]:
    """
    Fetches the unique organization IDs for which usage data is available in the database.

    Returns:
        List[int]: A list of integers representing the unique organization IDs.
    """
    logger.info("Fetching unique organization IDs")

    conn = psycopg2.connect(
        host="db", database=db_name, user=db_username, password=db_password
    )
    logger.info("Connected to database")

    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT org_id FROM usage ORDER BY org_id;")

    data = cursor.fetchall()

    org_ids = [row[0] for row in data]

    logger.info(f"Fetched {len(org_ids)} organization IDs from database")
    conn.close()

    return org_ids


@app.get("/organizations")
def get_org_ids() -> List[int]:
    """
    Endpoint that returns a list of unique organization IDs for which usage data is available in the database.

    Returns:
        List[int]: A list of integers representing the unique organization IDs.
    """

    logger.info("Received request for organization IDs")

    start_time = time.monotonic()

    org_ids = fetch_org_ids()

    response_time = time.monotonic() - start_time

    logger.info(f"Returning {len(org_ids)} organization IDs in {response_time:.2f}s")

    return org_ids
