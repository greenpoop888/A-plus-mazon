import React from 'react';
import { Table, Icon, Label } from 'semantic-ui-react';

const ProductItemRow = ({ product, stock }) => {
    const renderStockUI = () => {
        if (stock === null) {
            return (
                <span style={{ color: '#848484' }}>
                    <Icon name="circle notched" loading /> Loading...
                </span>
            );
        }

        if (stock <= 0) {
            return (
                <Label color="red" basic size="small">
                    <Icon name="minus circle" /> {stock}
                </Label>
            );
        }

        if (stock <= 10) {
            return (
                <Label color="orange" basic size="small">
                    <Icon name="hourglass half" /> {stock}
                </Label>
            );
        }

        return (
            <Label color="green" basic size="small">
                <Icon name="check circle" /> {stock}
            </Label>
        );
    };

    return (
        <Table.Row>
            <Table.Cell singleLine>
                <code>{product.barcode || 'N/A'}</code>
            </Table.Cell>

            <Table.Cell>
                <div style={{ fontWeight: 'bold' }}>{product.name}</div>
            </Table.Cell>

            <Table.Cell textAlign="right">
                ${product.price.toFixed(2)}
            </Table.Cell>

            <Table.Cell textAlign="center">
                {product.on_sale ? (
                    <Label color="red" horizontal size="mini">ON SALE</Label>
                ) : (
                    <span style={{ color: '#ccc' }}>-</span>
                )}
            </Table.Cell>

            <Table.Cell textAlign="right">
                {product.on_sale
                    ? `${(product.on_sale * 100).toFixed(0)}%`
                    : '-'}
            </Table.Cell>

            <Table.Cell textAlign="right">
                {product.product_line_name}
            </Table.Cell>

            <Table.Cell textAlign="center">
                {product.is_effectively_on_sale ? (
                    <Label color="red" horizontal size="mini">ON SALE</Label>
                ) : (
                    <span style={{ color: '#ccc' }}>-</span>
                )}
            </Table.Cell>

            <Table.Cell textAlign="right">
                {product.is_effectively_on_sale
                    ? `${(product.final_sale_rate * 100).toFixed(0)}%`
                    : '-'}
            </Table.Cell>

            <Table.Cell textAlign="center">
                {renderStockUI()}
            </Table.Cell>
        </Table.Row>
    );
};

export default ProductItemRow;