import React, { useState, useEffect } from 'react';
import { Card, Image, Message, Label, Icon } from 'semantic-ui-react';
import { getProducts } from '../services/api';

const Items = ({ store, primaryCategory, secondaryCategory, tertiaryCategory }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!store) {
            setProducts([]);
            setLoading(false);
            return;
        }

        const fetchProducts = async () => {
            try {
                setLoading(true);
                const filters = {};
                if (store) filters.store = store;
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
    }, [store, primaryCategory, secondaryCategory, tertiaryCategory]);

    if (loading) return <Message info>Loading products...</Message>;
    if (error) return <Message error>{error}</Message>;
    if (products.length === 0) return <Message warning>No products found.</Message>;

    return (
        <Card.Group itemsPerRow={3} stackable>
            {products.map((product) => (
                <Card key={product.id} style={{
                    height: '450px',
                    display: 'flex',
                    flexDirection: 'column'
                }}>
                    <div style={{
                        height: '200px',
                        width: '100%',
                        background: '#f0f0f000',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        overflow: 'hidden'
                    }}>
                        <Image
                            src={product.image_url}
                            style={{
                                maxHeight: '100%',
                                maxWidth: '100%',
                                objectFit: 'contain'
                            }}
                        />
                    </div>

                    <Card.Content style={{ flexGrow: 1, overflow: 'hidden' }}>
                        <Card.Header style={{ fontSize: '1.1em', height: '1.2em', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {product.name}
                        </Card.Header>
                        <Card.Meta style={{ color: '#f2711c', fontWeight: 'bold' }}>
                            ${product.price}
                        </Card.Meta>
                        <Card.Description style={{
                            height: '60px',
                            overflow: 'hidden',
                            display: '-webkit-box',
                            WebkitLineClamp: '3',
                            WebkitBoxOrient: 'vertical',
                            fontSize: '0.9em'
                        }}>
                            {product.description}
                        </Card.Description>

                        <div style={{ marginTop: '10px' }}>
                            <div style={{ fontSize: '0.85em', fontWeight: 'bold', color: '#555' }}>Ingredients:</div>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '4px' }}>
                                {product.ingredients?.map((ingredient, index) => (
                                    <Label key={index} size="mini" basic color="grey">
                                        {ingredient}
                                    </Label>
                                ))}
                            </div>
                        </div>
                    </Card.Content>

                    <Card.Content extra>
                        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', rowGap: '8px' }}>
                            {product.primary_category_id && (
                                <span style={{ display: 'flex', alignItems: 'center' }}>
                                    <Label size="tiny" color="blue">{product.primary_category_id}</Label>
                                    {product.secondary_category_id && <Icon name="chevron right" size="tiny" style={{ margin: '0 4px', color: '#ccc' }} />}
                                </span>
                            )}
                            {product.secondary_category_id && (
                                <span style={{ display: 'flex', alignItems: 'center' }}>
                                    <Label size="tiny">{product.secondary_category_id}</Label>
                                    {product.tertiary_category_id && <Icon name="chevron right" size="tiny" style={{ margin: '0 4px', color: '#ccc' }} />}
                                </span>
                            )}
                            {product.tertiary_category_id && (
                                <Label size="tiny" basic color="grey">{product.tertiary_category_id}</Label>
                            )}
                        </div>
                    </Card.Content>
                </Card>
            ))}
        </Card.Group>
    );
};

export default Items;