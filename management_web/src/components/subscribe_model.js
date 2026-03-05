import React, { useState, useEffect, useMemo } from 'react';
import { Modal, Button, Form, Radio, Dropdown, Divider } from 'semantic-ui-react';
import { subscribe, getCategories, getStores } from '../services/api';

const SubscribeModal = ({ isOpen, onClose, currentStoreId }) => {
    const [targetType, setTargetType] = useState('store');
    const [selectedStore, setSelectedStore] = useState(currentStoreId);
    const [frequency, setFrequency] = useState('day');
    const [stores, setStores] = useState([]);
    const [categories, setCategories] = useState([]);

    const [cat1, setCat1] = useState('');
    const [cat2, setCat2] = useState('');
    const [cat3, setCat3] = useState('');

    useEffect(() => {
        if (isOpen) {
            Promise.all([getStores(), getCategories()])
                .then(([transformedStores, transformedCategories]) => {
                    setStores(transformedStores);
                    setCategories(transformedCategories);
                    setSelectedStore(currentStoreId);
                })
                .catch(err => console.error(err));
        }
    }, [isOpen, currentStoreId]);

    const cat1Options = useMemo(() => {
        return categories.primary || [];
    }, [categories]);

    const cat2Options = useMemo(() => {
        if (!cat1 || !categories.secondary) return [];
        return categories.secondary[String(cat1)] || [];
    }, [categories, cat1]);

    const cat3Options = useMemo(() => {
        if (!cat2 || !categories.tertiary) return [];
        return categories.tertiary[String(cat2)] || [];
    }, [categories, cat2]);

    const handleSubmit = async () => {
        const deepestCategoryId = targetType === 'category' ? (cat3 || cat2 || cat1) : null;
        const finalStoreId = targetType === 'store' ? selectedStore : null;

        try {
            await subscribe(finalStoreId, deepestCategoryId, frequency);
            alert("Subscribed successfully!");
            onClose();
        } catch (error) {
            alert("Subscription failed.");
        }
    };

    return (
        <Modal open={isOpen} onClose={onClose} size='tiny'>
            <Modal.Header>Subscribe to Sales Report</Modal.Header>
            <Modal.Content>
                <Form>
                    <Form.Group inline>
                        <label>Report Target:</label>
                        <Form.Field>
                            <Radio label='Store' name='targetType' value='store'
                                checked={targetType === 'store'} onChange={() => setTargetType('store')} />
                        </Form.Field>
                        <Form.Field>
                            <Radio label='Category' name='targetType' value='category'
                                checked={targetType === 'category'} onChange={() => setTargetType('category')} />
                        </Form.Field>
                    </Form.Group>

                    <Divider />

                    {targetType === 'store' ? (
                        <Form.Field>
                            <label>Select Store</label>
                            <Dropdown placeholder='Select Store' fluid search selection
                                value={selectedStore}
                                options={stores}
                                onChange={(e, { value }) => setSelectedStore(value)}
                            />
                        </Form.Field>
                    ) : (
                        <>
                            <Form.Field>
                                <label>Category Level 1</label>
                                <Dropdown fluid selection placeholder='Main Category'
                                    options={cat1Options} value={cat1}
                                    onChange={(e, { value }) => { setCat1(value); setCat2(''); setCat3(''); }}
                                />
                            </Form.Field>
                            <Form.Field disabled={!cat1}>
                                <label>Category Level 2</label>
                                <Dropdown fluid selection placeholder='Sub Category'
                                    options={cat2Options} value={cat2}
                                    onChange={(e, { value }) => { setCat2(value); setCat3(''); }}
                                />
                            </Form.Field>
                            <Form.Field disabled={!cat2}>
                                <label>Category Level 3</label>
                                <Dropdown fluid selection placeholder='Specific Type'
                                    options={cat3Options} value={cat3}
                                    onChange={(e, { value }) => setCat3(value)}
                                />
                            </Form.Field>
                        </>
                    )}

                    <Divider />

                    <Form.Field>
                        <label>Update Frequency</label>
                        <Dropdown placeholder='Select Frequency' fluid selection
                            value={frequency} options={[
                                { key: 'm', text: 'By Minute', value: 'minute' },
                                { key: 'h', text: 'By Hour', value: 'hour' },
                                { key: 'd', text: 'By Day', value: 'day' },
                                { key: 'w', text: 'By Week', value: 'week' },
                                { key: 'mo', text: 'By Month', value: 'month' },
                            ]}
                            onChange={(e, { value }) => setFrequency(value)}
                        />
                    </Form.Field>
                </Form>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={onClose}>Cancel</Button>
                <Button color='teal' onClick={handleSubmit}
                    disabled={(targetType === 'category' && !cat1) || (targetType === 'store' && !selectedStore)}>
                    Confirm Subscription
                </Button>
            </Modal.Actions>
        </Modal>
    );
};

export default SubscribeModal;