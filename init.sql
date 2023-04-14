DROP DATABASE IF EXISTS geo_heatmap_db;

CREATE EXTENSION postgis;

CREATE DATABASE geo_heatmap_db;

GRANT ALL ON DATABASE TO geo_heatmap_user;

\c geo_heatmap_db;


