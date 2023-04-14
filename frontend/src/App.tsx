import React, { useState } from 'react';
import { Grid, Typography } from '@material-ui/core';
import { OrganizationSelector } from './components/OrganizationSelector';
import { HeatmapGenerator } from './components/HeatmapGenerator';
import { Heatmap } from './components/Heatmap';
import { Footer } from './components/Footer';

function App() {
  const [selectedOrg, setSelectedOrg] = useState<string>('all');
  const [heatmapData, setHeatmapData] = useState<any>(null);

  const handleOrganizationChange = (orgId: string) => {
    setSelectedOrg(orgId);
    setHeatmapData(null);
  };

  const handleHeatmapDataChange = (data: any) => {
    setHeatmapData(data);
  };

  return (
    <>
      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12}>
          <Typography variant="h4" align="center">
            Heatmap Generator
          </Typography>
        </Grid>
        <Grid item xs={3} >
          <OrganizationSelector onOrganizationChange={handleOrganizationChange} />
        </Grid>
        <Grid item xs={3}>
          <HeatmapGenerator selectedOrg={selectedOrg} onHeatmapDataChange={handleHeatmapDataChange} />
        </Grid>
        <Grid item xs={12} className='heatmap-container' style={{ height: '100%' }}>
          {heatmapData && <Heatmap heatmapData={heatmapData} />}
        </Grid>
      </Grid>
      <Grid container spacing={2} justifyContent="center">
        <Footer />
      </Grid>
    </>
  );
}

export default App;