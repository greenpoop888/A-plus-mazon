import React, { useState, useEffect } from 'react';
import { Table, Loader } from 'semantic-ui-react';
import { getProducts, getQuantities } from '../services/api';
import ProductItem from './product_item';

const Items = ({
    store,
    selectedIds,
    onSelectionChange,
    isEditMode,
    tempQuantities,
    onQtyMapChange,
    onOriginalStocksLoad
}) => {
    const [products, setProducts] = useState([]);
    const [stocks, setStocks] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!store) return;
        const fetchData = async () => {
            setLoading(true);
            try {
                const productData = await getProducts({ store });
                setProducts(productData);

                if (productData.length > 0) {
                    const stockData = await getQuantities(store, productData.map(p => p.id));
                    const stockMap = {};
                    stockData.forEach(item => {
                        stockMap[item.product_id] = item.quantity;
                    });

                    setStocks(stockMap);
                    onQtyMapChange(stockMap);

                    if (onOriginalStocksLoad) {
                        onOriginalStocksLoad(stockMap);
                    }
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [store]);

    const handleQtyChange = (pid, val) => {
        onQtyMapChange({ ...tempQuantities, [pid]: val });
    };

    if (loading) return <Loader active inline='centered' />;

    return (
        <Table celled padded selectable>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell textAlign="center">Select</Table.HeaderCell>
                    <Table.HeaderCell>Barcode</Table.HeaderCell>
                    <Table.HeaderCell>Product Name</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right">Price</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center">Sale</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right">Rate</Table.HeaderCell>
                    <Table.HeaderCell>Line</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center">Line Sale</Table.HeaderCell>
                    <Table.HeaderCell textAlign="right">Line Rate</Table.HeaderCell>
                    <Table.HeaderCell textAlign="center">Qty</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {products.map((product) => (
                    <ProductItem
                        key={product.id}
                        product={product}
                        stock={stocks[product.id]}
                        isSelected={selectedIds.includes(product.id)}
                        onSelect={(id) => onSelectionChange(
                            selectedIds.includes(id) ? selectedIds.filter(i => i !== id) : [...selectedIds, id]
                        )}
                        isEditMode={isEditMode}
                        editedQty={tempQuantities[product.id]}
                        onQtyChange={handleQtyChange}
                    />
                ))}
            </Table.Body>
        </Table>
    );
};

export default Items;