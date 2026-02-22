import React, { useState } from 'react';
import { Container, Header, Label, Segment, Grid, Button, Confirm } from 'semantic-ui-react';
import Items from '../components/items';
import Stories from '../components/store_selection';
import OfferModal from '../components/offer_item';
import { unofferProducts, updateQuantity } from '../services/api';

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
    const [originalStocks, setOriginalStocks] = useState({});

    const handleSaveAllClick = () => {
        setSaveConfirmOpen(true);
    };

    const confirmBulkUpdate = async () => {
        const hasNegative = Object.values(tempQuantities).some(qty => qty < 0);

        if (hasNegative) {
            alert("Quantity cannot be negative! Please check your inputs.");
            return;
        }

        setSaveConfirmOpen(false);

        const updates = Object.keys(tempQuantities)
            .filter(id => {
                const productId = Number(id);
                return tempQuantities[id] !== originalStocks[productId];
            })
            .map(id => ({
                product_id: Number(id),
                quantity: Number(tempQuantities[id])
            }));

        if (updates.length === 0) {
            alert("No changes detected.");
            setIsEditMode(false);
            return;
        }

        try {
            const response = await updateQuantity(Number(store), updates);

            if (response) {
                setIsEditMode(false);
                setRefreshKey(prev => prev + 1);
                alert(`Updated ${updates.length} item(s) successfully!`);
            }
        } catch (err) {
            console.error(err);
        }
    };

    const handleUnofferClick = () => {
        if (selectedIds.length === 0) return alert("Please select at least one product.");
        setConfirmOpen(true);
    };

    const handleConfirmUnoffer = async () => {
        try {
            const response = await unofferProducts(Number(store), selectedIds);

            if (response) {
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
                            <Header as='h1'><Label size='massive' color='orange'>A+mazon⟷ Management Portal</Label></Header>
                        </Grid.Column>
                        <Grid.Column width={6} textAlign='right'>
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
                onOriginalStocksLoad={setOriginalStocks}
                selectedIds={selectedIds}
                onSelectionChange={setSelectedIds}
            />

            <Confirm
                open={saveConfirmOpen}
                header="Confirm Update"
                content="Are you sure you want to update quantities for products in this list?"
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