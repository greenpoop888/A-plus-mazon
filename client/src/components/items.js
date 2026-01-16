import React, { useState, useEffect } from 'react';
import { Card, Image, Button, Message } from 'semantic-ui-react';
import { getProducts } from '../services/api';

const Items = ({ primaryCategory, secondaryCategory, tertiaryCategory }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                setLoading(true);
                const filters = {};

                if (primaryCategory) filters.primary_category = primaryCategory;
                if (secondaryCategory) filters.secondary_category = secondaryCategory;
                if (tertiaryCategory) filters.tertiary_category = tertiaryCategory;

                const productData = await getProducts(filters);
                setProducts(productData);
                setError(null);
            } catch (err) {
                console.error('Error fetching products:', err);
                setError('Failed to load products');
                setProducts([]);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, [primaryCategory, secondaryCategory, tertiaryCategory]);

    if (loading) {
        return <Message info>Loading products...</Message>;
    }

    if (error) {
        return <Message error>{error}</Message>;
    }

    if (products.length === 0) {
        return <Message warning>No products found for the selected categories.</Message>;
    }

    return (
        <Card.Group itemsPerRow={3} stackable>
            {products.map((product) => (
                <Card key={product.id}>
                    <Image src={product.image_url} wrapped ui={false} />
                    <Card.Content>
                        <Card.Header>{product.name}</Card.Header>
                        <Card.Meta>${product.price}</Card.Meta>
                        <Card.Description>{product.description}</Card.Description>
                    </Card.Content>
                    <Card.Content extra>
                        <Button primary>Add to Cart</Button>
                    </Card.Content>
                </Card>
            ))}
        </Card.Group>
    );
};

export default Items;