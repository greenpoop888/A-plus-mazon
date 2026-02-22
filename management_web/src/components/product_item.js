import React from 'react';
import { Table, Icon, Label, Checkbox, Input } from 'semantic-ui-react';

const ProductItemRow = ({ product, stock, isSelected, onSelect, isEditMode, editedQty, onQtyChange }) => {
    const renderStockUI = () => {
        if (isEditMode) {
            return (
                <Input
                    type="number"
                    size="mini"
                    style={{ width: '80px' }}
                    min={0}
                    value={editedQty !== undefined ? editedQty : (stock || 0)}
                    onChange={(e) => onQtyChange(product.id, Number(e.target.value))}
                />
            );
        }

        if (stock === null) return <span><Icon name="circle notched" loading /></span>;
        const color = stock <= 0 ? "red" : (stock <= 10 ? "orange" : "green");
        return <Label color={color} basic size="small">{stock}</Label>;
    };

    return (
        <Table.Row active={isSelected}>
            <Table.Cell textAlign="center">
                <Checkbox checked={isSelected} onChange={() => onSelect(product.id)} />
            </Table.Cell>
            <Table.Cell><code>{product.barcode || 'N/A'}</code></Table.Cell>
            <Table.Cell><b>{product.name}</b></Table.Cell>
            <Table.Cell textAlign="right">${product.price.toFixed(2)}</Table.Cell>
            <Table.Cell textAlign="center">
                {product.on_sale ? <Label color="red" horizontal size="mini">ON SALE</Label> : '-'}
            </Table.Cell>
            <Table.Cell textAlign="right">{product.on_sale ? `${(product.on_sale * 100).toFixed(0)}%` : '-'}</Table.Cell>
            <Table.Cell>{product.product_line_name}</Table.Cell>
            <Table.Cell textAlign="center">
                {product.is_effectively_on_sale ? <Label color="red" horizontal size="mini">ON SALE</Label> : '-'}
            </Table.Cell>
            <Table.Cell textAlign="right">{product.is_effectively_on_sale ? `${(product.final_sale_rate * 100).toFixed(0)}%` : '-'}</Table.Cell>
            <Table.Cell textAlign="center">{renderStockUI()}</Table.Cell>
        </Table.Row>
    );
};

export default ProductItemRow;