import React, { useState, useEffect } from 'react';
import { Dropdown, Button } from 'semantic-ui-react';
import { getStores as getStores } from '../services/api';

const Stories = () => {
    const [stores, setStores] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedStore, setSelectedStore] = useState('');

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                setLoading(true);
                const storeData = await getStores();

                const transformed = storeData.map(store => ({
                    key: store.id,
                    text: store.name,
                    value: store.id
                }));

                setStores(transformed);
                setError(null);
            } catch (err) {
                console.error('Error fetching categories:', err);
                setError('Failed to load categories');
            } finally {
                setLoading(false);
            }
        };

        fetchCategories();
    }, []);

    const handleStoreChange = (e, { value }) => {
        setSelectedStore(value);
    };

    const handleReset = () => {
        setSelectedStore('');
    };

    if (loading) return <div>Loading Store...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <Dropdown
                placeholder='Select Store'
                search
                selection
                options={stores}
                value={selectedStore}
                onChange={handleStoreChange}
                style={{ marginRight: '10px' }}
            />
            <Button onClick={handleReset} color='orange'>Reset</Button>
        </div>
    );
};

export default Stories;