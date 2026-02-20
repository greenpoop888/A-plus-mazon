import React, { useState } from 'react';
import { Container, Header, Label, Segment, Grid, Button, Confirm } from 'semantic-ui-react';
import Items from '../components/items';
import Stories from '../components/store_selection';
import OfferModal from '../components/offer_item';
import { unofferProducts } from '../services/api';

const Home = () => {
    const [store, setStore] = useState('');
    const [storeOptions, setStoreOptions] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedIds, setSelectedIds] = useState([]);
    const [confirmOpen, setConfirmOpen] = useState(false);
    const [refreshKey, setRefreshKey] = useState(0);
    const currentStoreName = storeOptions.find(s => s.value === store)?.text || store;
    const [isEditMode, setIsEditMode] = useState(false);
    const [tempQuantities, setTempQuantities] = useState({});
    const [saveConfirmOpen, setSaveConfirmOpen] = useState(false);

    const handleSaveAllClick = () => {
        setSaveConfirmOpen(true);
    };

    const confirmBulkUpdate = async () => {
        setSaveConfirmOpen(false);
        const updates = Object.keys(tempQuantities).map(id => ({
            product_id: Number(id),
            quantity: Number(tempQuantities[id])
        }));

        try {
            const response = await fetch('/api/products/bulk-update', { // 假設你的路徑
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    store_id: Number(store),
                    updates: updates
                })
            });

            if (response.ok) {
                setIsEditMode(false);
                setRefreshKey(prev => prev + 1);
                alert("All quantities updated!");
            }
        } catch (err) { console.error(err); }
    };

    const handleUnofferClick = () => {
        if (selectedIds.length === 0) return alert("Please select at least one product.");
        setConfirmOpen(true);
    };

    const handleConfirmUnoffer = async () => {
        try {
            const response = await fetch('/api/products', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    store_id: Number(store),
                    product_ids: selectedIds
                })
            });

            if (response.ok) {
                setConfirmOpen(false);
                setSelectedIds([]);
                setRefreshKey(prev => prev + 1);

                alert("Products removed successfully.");
            } else {
                const errorData = await response.json();
                alert(`Failed: ${errorData.detail || "Unknown error"}`);
                setConfirmOpen(false);
            }
        } catch (error) {
            console.error("Delete error:", error);
            alert("Network error.");
            setConfirmOpen(false);
        }
    };

    return (
        <Container>
            <Segment>
                <Grid verticalAlign='middle'>
                    <Grid.Row>
                        <Grid.Column width={10}>
                            <Header as='h1'><Label size='massive' color='orange'>A+mazon⟷ Management site</Label></Header>
                        </Grid.Column>
                        <Grid.Column width={6}>
                            <Stories
                                store={store}
                                onStoreChange={setStore}
                                onStoresLoad={setStoreOptions}
                            />
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <Button color='green' onClick={() => setIsModalOpen(true)}>Offer new product</Button>
                            <Button
                                color='red'
                                onClick={handleUnofferClick}
                                disabled={selectedIds.length === 0}
                            >
                                Unoffer ({selectedIds.length})
                            </Button>
                            {!isEditMode ? (
                                <Button color='blue' onClick={() => setIsEditMode(true)}>Edit Quantity</Button>
                            ) : (
                                <>
                                    <Button color='orange' onClick={handleSaveAllClick} icon='save' content='Save All Changes' />
                                    <Button onClick={() => setIsEditMode(false)}>Cancel</Button>
                                </>
                            )}
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Segment>

            <Items
                key={refreshKey}
                store={store}
                isEditMode={isEditMode}
                tempQuantities={tempQuantities}
                onQtyMapChange={setTempQuantities}
                selectedIds={selectedIds}
                onSelectionChange={setSelectedIds}
            />

            <Confirm
                open={saveConfirmOpen}
                header="Confirm Bulk Update"
                content="Are you sure you want to update quantities for ALL products in this list?"
                onCancel={() => setSaveConfirmOpen(false)}
                onConfirm={confirmBulkUpdate}
            />

            <OfferModal
                store={store}
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onRefresh={() => setRefreshKey(old => old + 1)}
            />

            <Confirm
                open={confirmOpen}
                header="Confirm Unoffer"
                content={
                    <div className="content" style={{ padding: '1.5rem', fontSize: '1.1rem' }}>
                        Are you sure you want to
                        <strong style={{ color: '#db2828', margin: '0 5px' }}>
                            unoffer {selectedIds.length} product(s)
                        </strong>
                        from
                        <strong style={{ color: '#db2828', marginLeft: '5px' }}>
                            {currentStoreName}
                        </strong>?
                    </div>
                }
                onCancel={() => setConfirmOpen(false)}
                onConfirm={handleConfirmUnoffer}
                cancelButton='No, keep them'
                confirmButton='Yes, remove from store'
            />
        </Container>
    );
};

export default Home;