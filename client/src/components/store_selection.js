import React, { useEffect, useState } from 'react';
import { Dropdown } from 'semantic-ui-react';
import { getStores } from '../services/api';


const Stories = ({ store, onStoreChange }) => {
    const [stores, setStores] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStoresData = async () => {
            try {
                const storeData = await getStores();
                const transformed = storeData.map(s => ({
                    key: s.id,
                    text: s.name,
                    value: s.id
                }));
                setStores(transformed);

                if (transformed.length > 0 && !store) {
                    onStoreChange(transformed[0].value);
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchStoresData();
    }, []);

    const handleDropdownChange = (e, { value }) => {
        if (value !== store) {
            onStoreChange(value);
        }
    };

    if (loading) return <span>Loading...</span>;

    return (
        <Dropdown
            button
            className='icon'
            floating
            labeled
            icon='warehouse'
            options={stores}
            search
            text={stores.find(s => s.value === store)?.text || 'Select Store'}
            onChange={handleDropdownChange}
        />
    );
};

export default Stories;