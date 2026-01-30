import React, { useState, useEffect } from 'react';
import { Card, Message } from 'semantic-ui-react';
import { getProducts, getQuantities } from '../services/api';
import ProductItem from './ProductItem';

const Items = ({ store, primaryCategory, secondaryCategory, tertiaryCategory }) => {
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
                const filters = {
                    store,
                    primary_category: primaryCategory,
                    secondary_category: secondaryCategory,
                    tertiary_category: tertiaryCategory
                };

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
                setError('Fetch error');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [store, primaryCategory, secondaryCategory, tertiaryCategory]);

    if (loading) return <Message info>Loading products...</Message>;
    if (error) return <Message error>{error}</Message>;
    if (products.length === 0) return <Message warning>No products found.</Message>;

    return (
        <Card.Group itemsPerRow={3} stackable>
            {products.map((product) => (
                <ProductItem
                    key={product.id}
                    product={product}
                    stock={stocks[product.id] !== undefined ? stocks[product.id] : null}
                />
            ))}
        </Card.Group>
    );
};

export default Items;