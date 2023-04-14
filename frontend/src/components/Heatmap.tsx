import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import { Typography } from '@material-ui/core';
import * as L from "leaflet";
import 'leaflet.heat';
import 'leaflet/dist/leaflet.css';


type HeatmapProps = {
    heatmapData: any;
};

const HeatmapLayer = ({ heatmapData }: HeatmapProps) => {
    const map = useMap();
    const [heatLayer, setHeatLayer] = useState<L.HeatLayer | null>(null);

    useEffect(() => {
        if (!heatLayer) {
            const layer = L.heatLayer([], { radius: 10, maxZoom: 1 }).addTo(map);
            setHeatLayer(layer);
        } else {
            const points = heatmapData.map(
                (point: any) => [point.lat, point.lng, point.weight] as [number, number, number]
            );
            heatLayer.setLatLngs(points);
        }
    }, [heatLayer, heatmapData, map]);

    return null;
};

export const Heatmap = ({ heatmapData }: HeatmapProps) => {
    const [mapCenter, setMapCenter] = useState<[number, number]>([0, 0]);

    useEffect(() => {
        if (heatmapData.length > 0) {
            const firstPoint = heatmapData[0];
            setMapCenter([firstPoint.lat, firstPoint.lng]);
        }
    }, [heatmapData]);

    return (
        <MapContainer center={mapCenter} zoom={1} style={{ height: "300px" }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <HeatmapLayer heatmapData={heatmapData} />
        </MapContainer>
    );
};
