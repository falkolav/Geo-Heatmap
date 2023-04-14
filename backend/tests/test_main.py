import os
import psycopg2
from fastapi.testclient import TestClient
from unittest import mock
from app.main import app, fetch_usage_data
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_name = "geo_heatmap_db"


def test_fetch_usage_data_all():
    with mock.patch("psycopg2.connect") as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [(1.2345, 6.7890, 10)]
        result = fetch_usage_data("all")
        assert result == [(1.2345, 6.7890, 10)]
        mock_connect.assert_called_once_with(
            host="localhost", database=db_name, user=db_username, password=db_password
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM centroid_usage GROUP BY centroid;"
        )


def test_fetch_usage_data_org_id():
    with mock.patch("psycopg2.connect") as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [(1.2345, 6.7890, 5)]
        result = fetch_usage_data("5")
        assert result == [(1.2345, 6.7890, 5)]
        mock_connect.assert_called_once_with(
            host="localhost", database=db_name, user=db_username, password=db_password
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM centroid_usage WHERE org_id = 5 GROUP BY centroid;"
        )


def test_get_heatmap_data_all():
    with mock.patch(
        "app.main.fetch_usage_data",
        return_value=[(51.12345, -1.23456, 10), (51.23456, -1.34567, 5)],
    ) as mock_fetch_usage_data:
        response = client.get("/heatmap-data/all")
        assert response.status_code == 200
        assert response.json() == [
            {"lat": 51.12345, "lng": -1.23456, "weight": 10},
            {"lat": 51.23456, "lng": -1.34567, "weight": 5},
        ]
        mock_fetch_usage_data.assert_called_once_with("all")


def test_get_heatmap_data_org_id():
    with mock.patch(
        "app.main.fetch_usage_data",
        return_value=[(51.12345, -1.23456, 10), (51.23456, -1.34567, 5)],
    ) as mock_fetch_usage_data:
        response = client.get("/heatmap-data/5")
        assert response.status_code == 200
        assert response.json() == [
            {"lat": 51.12345, "lng": -1.23456, "weight": 10},
            {"lat": 51.23456, "lng": -1.34567, "weight": 5},
        ]
        mock_fetch_usage_data.assert_called_once_with("5")


@mock.patch("psycopg2.connect")
def test_fetch_usage_data(mock_connect):
    mock_cursor = mock_connect.return_value.cursor.return_value

    mock_cursor.fetchall.return_value = [(1.2345, 6.7890, 10)]

    result = fetch_usage_data("all")

    assert result == [(1.2345, 6.7890, 10)]

    mock_connect.assert_called_once_with(
        host="localhost", database=db_name, user=db_username, password=db_password
    )
    mock_cursor.execute.assert_called_once_with(
        "SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM centroid_usage GROUP BY centroid;"
    )

    mock_connect.reset_mock()
    mock_cursor.reset_mock()

    mock_cursor.fetchall.return_value = [(1.2345, 6.7890, 5)]

    result = fetch_usage_data("5")

    assert result == [(1.2345, 6.7890, 5)]

    mock_connect.assert_called_once_with(
        host="localhost",
        database=db_name,
        user=db_username,
        password=db_password,
    )
    mock_cursor.execute.assert_called_once_with(
        "SELECT ST_Y(centroid) as lat, ST_X(centroid) as lng, COUNT(*) as weight FROM centroid_usage WHERE org_id = 5 GROUP BY centroid;"
    )


@mock.patch("psycopg2.connect")
def test_fetch_usage_data_exception(mock_connect):
    mock_connect.side_effect = psycopg2.OperationalError()

    with pytest.raises(Exception):
        fetch_usage_data("all")


def test_get_heatmap_data():
    # Test with all organizations
    with mock.patch(
        "app.main.fetch_usage_data",
        return_value=[(51.12345, -1.23456, 10), (51.23456, -1.34567, 5)],
    ) as mock_fetch_usage_data:
        response = client.get("/heatmap-data/all")
        assert response.status_code == 200
        assert response.json() == [
            {"lat": 51.12345, "lng": -1.23456, "weight": 10},
            {"lat": 51.23456, "lng": -1.34567, "weight": 5},
        ]
        mock_fetch_usage_data.assert_called_once_with("all")

    # Test with specific organization
    with mock.patch(
        "app.main.fetch_usage_data",
        return_value=[(51.12345, -1.23456, 10), (51.23456, -1.34567, 5)],
    ) as mock_fetch_usage_data:
        response = client.get("/heatmap-data/5")
        assert response.status_code == 200
        assert response.json() == [
            {"lat": 51.12345, "lng": -1.23456, "weight": 10},
            {"lat": 51.23456, "lng": -1.34567, "weight": 5},
        ]
        mock_fetch_usage_data.assert_called_once_with("5")
