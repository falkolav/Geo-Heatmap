import React from 'react';
import { Grid, Typography, Link } from '@material-ui/core';

export function Footer() {
    return (
        <Grid item xs={12} >
            <Typography variant="body2" align="center" >
                Made by Falko Lavitt. Full code available{' '}
                <Link href="https://github.com/falkolav/">here</Link>.
            </Typography>
        </Grid>
    );
}