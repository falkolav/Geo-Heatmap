import React, { useState } from 'react';
import { Button } from '@material-ui/core';
import { fetchHeatmapData } from '../api';

type HeatmapGeneratorProps = {
    selectedOrg: string;
    onHeatmapDataChange: (data: any) => void;
};

export const HeatmapGenerator = ({ selectedOrg, onHeatmapDataChange }: HeatmapGeneratorProps) => {
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleGenerateHeatmap = async () => {
        setIsLoading(true);
        const heatmapData = await fetchHeatmapData(selectedOrg);
        setIsLoading(false);
        onHeatmapDataChange(heatmapData);
    };

    return (
        <Button
            variant="contained"
            color="primary"
            disabled={!selectedOrg}
            onClick={handleGenerateHeatmap}
        >
            {isLoading ? 'Loading...' : 'Generate Heatmap'}
        </Button>
    );
};
