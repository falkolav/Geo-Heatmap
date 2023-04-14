import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const fetchOrganizations = async () => {
    const response = await axios.get(`${API_BASE_URL}/organizations`);
    return response.data;
};

export const fetchHeatmapData = async (orgId: string) => {
    const response = await axios.get(`${API_BASE_URL}/heatmap-data/${orgId}`);
    return response.data;
};

export { };