import React, { useEffect, useState } from 'react';
import { Dropdown } from 'semantic-ui-react';
import { getStores } from '../services/api';


const Stories = ({ store, onStoreChange, onStoresLoad }) => {
    const [stores, setStores] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStoresData = async () => {
            try {
                const storeData = await getStores();
                setStores(storeData);

                if (onStoresLoad) onStoresLoad(storeData);

                if (storeData.length > 0 && !store) {
                    onStoreChange(storeData[0].value);
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