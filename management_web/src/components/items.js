import React, { useState, useEffect } from 'react';
import { Table, Message, Icon } from 'semantic-ui-react';
import { getProducts, getQuantities } from '../services/api';
import ProductItem from './ProductItem';

const Items = ({ store }) => {
    const [products, setProducts] = useState([]);
    const [stocks, setStocks] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!store) {
            setProducts([]);
            setLoading(false);
            return;
        }

        const fetchData = async () => {
            try {
                setLoading(true);
                const filters = { store };

                const productData = await getProducts(filters);
                setProducts(productData);

                if (productData.length > 0) {
                    const productIds = productData.map(p => p.id);
                    const stockData = await getQuantities(store, productIds);

                    const stockMap = {};
                    stockData.forEach(item => {
                        stockMap[item.product_id] = item.quantity;
                    });
                    setStocks(stockMap);
                }

                setError(null);
            } catch (err) {
                console.error('Fetch error:', err);
                setError('Error fetching products or stocks. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [store]);

    if (loading) return <Message info><Icon name='circle notched' loading /> Loading products...</Message>;
    if (error) return <Message error>{error}</Message>;
    if (products.length === 0) return <Message warning>No items found for this store.</Message>;

    return (
        <Table celled padded selectable stackable>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell width={1}>Barcode</Table.HeaderCell>
                    <Table.HeaderCell width={1}>Product Name</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right" width={1}>Price</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center" width={1}>Product On Sale</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right" width={1}>Product Sale Rate</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center" width={1}>Product Line</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center" width={1}>Product Line On Sale</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right" width={1}>Product Line Sale Rate</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right" width={1}>System Qty</Table.HeaderCell>
                </Table.Row>
            </Table.Header>

            <Table.Body>
                {products.map((product) => (
                    <ProductItem
                        key={product.id}
                        product={product}
                        stock={stocks[product.id] !== undefined ? stocks[product.id] : null}
                    />
                ))}
            </Table.Body>
        </Table>
    );
};

export default Items;