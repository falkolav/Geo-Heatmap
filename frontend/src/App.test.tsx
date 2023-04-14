import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('App', () => {
    it('renders the title', () => {
        render(<App />);
        const title = screen.getByText('Heatmap Generator');
        expect(title).toBeInTheDocument();
    });

    it('renders the OrganizationSelector component', () => {
        render(<App />);
        const organizationSelector = screen.getByText(/Organization/);
        expect(organizationSelector).toBeInTheDocument();
    });

    it('renders the HeatmapGenerator component', () => {
        render(<App />);
        const heatmapGenerator = screen.getByText(/Generate Heatmap/);
        expect(heatmapGenerator).toBeInTheDocument();
    });

    it('renders the Footer component', () => {
        render(<App />);
        const footer = screen.getByText(/Made by Falko Lavitt. Full code available/);
        expect(footer).toBeInTheDocument();
    });
});