import React from 'react';
import { Card, Image, Label, Icon } from 'semantic-ui-react';

const ProductItem = ({ product, stock }) => {
    const renderStockInfo = () => {
        if (stock === null) return 'Loading...';
        return stock > 0 ? `${stock} in stock` : 'Out of stock';
    };

    const renderStockUI = () => {
        if (stock === null) {
            return (
                <span style={{ color: '#848484', fontWeight: 'bold' }}>
                    <Icon name="circle notched" loading /> Loading...
                </span>
            );
        }

        if (stock <= 0) {
            return (
                <span style={{ color: '#848484', fontWeight: 'bold' }}>
                    <Icon name="minus circle" /> Out of stock
                </span>
            );
        }

        if (stock <= 10) {
            return (
                <span style={{ color: '#ff851b', fontWeight: 'bold' }}>
                    <Icon name="hourglass half" /> Only {stock} left
                </span>
            );
        }

        return (
            <span style={{ color: '#000000', fontWeight: 'bold' }}>
                <Icon name="check circle" color="green" /> In stock
            </span>
        );
    };

    return (
        <Card style={{ height: '450px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ height: '200px', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
                <Image src={product.image_url} style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain' }} />
            </div>

            <Card.Content style={{ flexGrow: 1, overflow: 'hidden' }}>
                <Card.Header style={{ fontSize: '1.1em', height: '1.2em', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {product.name}
                </Card.Header>

                <Card.Meta>
                    <span style={{ color: product.is_effectively_on_sale ? '#848484' : '#000000', fontWeight: 'bold', textDecoration: product.is_effectively_on_sale ? 'line-through' : 'none' }}>
                        ${product.price}
                    </span>
                    {product.is_effectively_on_sale && (
                        <span style={{ color: '#ff0000', fontWeight: 'bold', marginLeft: '5px' }}>
                            ${(product.price * product.final_sale_rate).toFixed(2)}
                        </span>
                    )}
                </Card.Meta>

                <Card.Meta>
                    {renderStockUI()}
                </Card.Meta>

                <Card.Description style={{ height: '60px', overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: '3', WebkitBoxOrient: 'vertical', fontSize: '0.9em' }}>
                    {product.description}
                </Card.Description>

            </Card.Content>

            <Card.Content extra>
            </Card.Content>
        </Card>
    );
};


export default ProductItem;