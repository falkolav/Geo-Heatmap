import React, { useState, useEffect } from 'react';
import { FormControl, InputLabel, MenuItem, Select } from '@material-ui/core';
import { fetchOrganizations } from '../api';

type OrganizationSelectorProps = {
    onOrganizationChange: (orgId: string) => void;
};

export const OrganizationSelector = ({ onOrganizationChange }: OrganizationSelectorProps) => {
    const [organizations, setOrganizations] = useState<string[]>([]);
    const [selectedOrg, setSelectedOrg] = useState<string>('all');

    useEffect(() => {
        const fetchOrganizationsAsync = async () => {
            const fetchedOrganizations = await fetchOrganizations();
            setOrganizations(['all', ...fetchedOrganizations.map((orgId: string) => orgId.toString())]);
        };
        fetchOrganizationsAsync();
    }, []);

    const handleOrganizationChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const selectedOrg = event.target.value as string;
        setSelectedOrg(selectedOrg);
        onOrganizationChange(selectedOrg);
    };

    return (
        <FormControl fullWidth>
            <InputLabel aria-label="organization-input">Organization</InputLabel>
            <Select value={selectedOrg} onChange={handleOrganizationChange}>
                {organizations.map((org) => (
                    <MenuItem key={org} value={org}>
                        {org}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};
