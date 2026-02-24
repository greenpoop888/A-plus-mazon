import React, { useState, useEffect } from 'react';
import {
    Modal,
    Table,
    Checkbox,
    Input,
    Button,
    Segment,
    Header,
    Icon,
    Loader,
    Message
} from 'semantic-ui-react';
import { getUnofferedProducts, offerProducts } from '../services/api';

const OfferModal = ({ store, isOpen, onClose, onRefresh }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);
    const [selectedItems, setSelectedItems] = useState({});

    useEffect(() => {
        if (isOpen && store) {
            fetchData();
        }
    }, [isOpen, store]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await getUnofferedProducts(store);
            setProducts(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleCheckboxChange = (productId) => {
        const newSelected = { ...selectedItems };
        if (newSelected[productId] !== undefined) {
            delete newSelected[productId];
        } else {
            newSelected[productId] = 1;
        }
        setSelectedItems(newSelected);
    };

    const handleQuantityChange = (productId, val) => {
        const qty = parseInt(val) || 0;
        if (selectedItems[productId] !== undefined) {
            setSelectedItems({ ...selectedItems, [productId]: qty >= 0 ? qty : 0 });
        }
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        const new_offer = Object.keys(selectedItems).map(id => ({
            product_id: Number(id),
            quantity: Number(selectedItems[id])
        }));

        try {
            const response = await offerProducts(store, new_offer);

            if (response) {
                setShowSuccess(true);
                setTimeout(() => {
                    setShowSuccess(false);
                    setSelectedItems({});
                    onClose();
                    onRefresh();
                }, 1500);
            }
        } catch (error) {
            console.error(error);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <Modal open={isOpen} onClose={onClose} size="large">
            <Modal.Header>Offer New Products</Modal.Header>
            <Modal.Content scrolling>
                {showSuccess ? (
                    <Segment placeholder textAlign="center" style={{ border: 'none', boxShadow: 'none' }}>
                        <Header icon>
                            <Icon name='check circle' color='green' />
                            Success!
                            <Header.Subheader>
                                Products have been added to your store.
                            </Header.Subheader>
                        </Header>
                    </Segment>
                ) : (
                    <>
                        {loading ? (
                            <Loader active inline='centered'>Loading products...</Loader>
                        ) : products.length > 0 ? (
                            <Table celled>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell width={1}>Select</Table.HeaderCell>
                                        <Table.HeaderCell>Product Name</Table.HeaderCell>
                                        <Table.HeaderCell>Category</Table.HeaderCell>
                                        <Table.HeaderCell width={3}>Quantity</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    {products.map((p) => (
                                        <Table.Row key={p.id}>
                                            <Table.Cell>
                                                <Checkbox
                                                    checked={selectedItems[p.id] !== undefined}
                                                    onChange={() => handleCheckboxChange(p.id)}
                                                />
                                            </Table.Cell>
                                            <Table.Cell>{p.name}</Table.Cell>
                                            <Table.Cell>{p.category}</Table.Cell>
                                            <Table.Cell>
                                                <Input
                                                    type="number"
                                                    min="0"
                                                    disabled={selectedItems[p.id] === undefined}
                                                    value={selectedItems[p.id] || ''}
                                                    onChange={(e) => handleQuantityChange(p.id, e.target.value)}
                                                />
                                            </Table.Cell>
                                        </Table.Row>
                                    ))}
                                </Table.Body>
                            </Table>
                        ) : (
                            <Message info content="No unoffered products available for this store." />
                        )}
                    </>
                )}
            </Modal.Content>
            {!showSuccess && (
                <Modal.Actions>
                    <Button onClick={onClose} disabled={submitting}>Cancel</Button>
                    <Button
                        positive
                        loading={submitting}
                        disabled={Object.keys(selectedItems).length === 0}
                        onClick={handleSubmit}
                    >
                        Confirm Offer
                    </Button>
                </Modal.Actions>
            )}
        </Modal>
    );
};

export default OfferModal;