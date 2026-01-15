import React from 'react';
import { Card, Image, Button } from 'semantic-ui-react';

const products = [
    {
        id: 1,
        name: 'Wireless Headphones',
        description: 'High-quality wireless headphones with noise cancellation.',
        price: '$99.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
    {
        id: 2,
        name: 'Smartphone Case',
        description: 'Durable case for your smartphone with stylish design.',
        price: '$19.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
    {
        id: 3,
        name: 'Laptop Stand',
        description: 'Adjustable laptop stand for better ergonomics.',
        price: '$49.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
    {
        id: 4,
        name: 'Bluetooth Speaker',
        description: 'Portable Bluetooth speaker with excellent sound quality.',
        price: '$79.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
    {
        id: 5,
        name: 'USB Charger',
        description: 'Fast-charging USB charger compatible with multiple devices.',
        price: '$14.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
    {
        id: 6,
        name: 'Gaming Mouse',
        description: 'Ergonomic gaming mouse with customizable buttons.',
        price: '$39.99',
        image: 'https://react.semantic-ui.com/images/avatar/large/matthew.png',
    },
];

const Items = () => {
    return (
        <Card.Group itemsPerRow={3} stackable>
            {products.map((product) => (
                <Card key={product.id}>
                    <Image src={product.image} wrapped ui={false} />
                    <Card.Content>
                        <Card.Header>{product.name}</Card.Header>
                        <Card.Meta>{product.price}</Card.Meta>
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