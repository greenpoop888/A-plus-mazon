import React, { useState } from 'react';
import { Dropdown } from 'semantic-ui-react';

const categories = {
    primary: [
        { key: 'electronics', text: 'Electronics', value: 'electronics' },
        { key: 'clothing', text: 'Clothing', value: 'clothing' },
        { key: 'books', text: 'Books', value: 'books' },
    ],
    secondary: {
        electronics: [
            { key: 'phones', text: 'Phones', value: 'phones' },
            { key: 'laptops', text: 'Laptops', value: 'laptops' },
            { key: 'accessories', text: 'Accessories', value: 'accessories' },
        ],
        clothing: [
            { key: 'shirts', text: 'Shirts', value: 'shirts' },
            { key: 'pants', text: 'Pants', value: 'pants' },
            { key: 'shoes', text: 'Shoes', value: 'shoes' },
        ],
        books: [
            { key: 'fiction', text: 'Fiction', value: 'fiction' },
            { key: 'non-fiction', text: 'Non-Fiction', value: 'non-fiction' },
            { key: 'textbooks', text: 'Textbooks', value: 'textbooks' },
        ],
    },
    tertiary: {
        phones: [
            { key: 'android', text: 'Android', value: 'android' },
            { key: 'ios', text: 'iOS', value: 'ios' },
            { key: 'feature-phones', text: 'Feature Phones', value: 'feature-phones' },
        ],
        laptops: [
            { key: 'gaming', text: 'Gaming', value: 'gaming' },
            { key: 'business', text: 'Business', value: 'business' },
            { key: 'ultrabook', text: 'Ultrabook', value: 'ultrabook' },
        ],
        accessories: [
            { key: 'chargers', text: 'Chargers', value: 'chargers' },
            { key: 'cases', text: 'Cases', value: 'cases' },
            { key: 'headphones', text: 'Headphones', value: 'headphones' },
        ],
        shirts: [
            { key: 't-shirts', text: 'T-Shirts', value: 't-shirts' },
            { key: 'button-ups', text: 'Button-Ups', value: 'button-ups' },
            { key: 'polos', text: 'Polos', value: 'polos' },
        ],
        pants: [
            { key: 'jeans', text: 'Jeans', value: 'jeans' },
            { key: 'khakis', text: 'Khakis', value: 'khakis' },
            { key: 'shorts', text: 'Shorts', value: 'shorts' },
        ],
        shoes: [
            { key: 'sneakers', text: 'Sneakers', value: 'sneakers' },
            { key: 'boots', text: 'Boots', value: 'boots' },
            { key: 'sandals', text: 'Sandals', value: 'sandals' },
        ],
        fiction: [
            { key: 'mystery', text: 'Mystery', value: 'mystery' },
            { key: 'romance', text: 'Romance', value: 'romance' },
            { key: 'sci-fi', text: 'Sci-Fi', value: 'sci-fi' },
        ],
        'non-fiction': [
            { key: 'biography', text: 'Biography', value: 'biography' },
            { key: 'history', text: 'History', value: 'history' },
            { key: 'self-help', text: 'Self-Help', value: 'self-help' },
        ],
        textbooks: [
            { key: 'math', text: 'Math', value: 'math' },
            { key: 'science', text: 'Science', value: 'science' },
            { key: 'literature', text: 'Literature', value: 'literature' },
        ],
    },
};

const DropdownExampleSearchSelectionTwo = () => {
    const [selectedPrimary, setSelectedPrimary] = useState('');
    const [selectedSecondary, setSelectedSecondary] = useState('');
    const [selectedTertiary, setSelectedTertiary] = useState('');

    const handlePrimaryChange = (e, { value }) => {
        setSelectedPrimary(value);
        setSelectedSecondary('');
        setSelectedTertiary('');
    };

    const handleSecondaryChange = (e, { value }) => {
        setSelectedSecondary(value);
        setSelectedTertiary('');
    };

    const handleTertiaryChange = (e, { value }) => {
        setSelectedTertiary(value);
    };

    const secondaryOptions = selectedPrimary ? categories.secondary[selectedPrimary] || [] : [];
    const tertiaryOptions = selectedSecondary ? categories.tertiary[selectedSecondary] || [] : [];

    return (
        <div>
            <Dropdown
                placeholder='Select Primary Category'
                search
                selection
                options={categories.primary}
                value={selectedPrimary}
                onChange={handlePrimaryChange}
                style={{ marginRight: '10px' }}
            />
            <Dropdown
                placeholder='Select Secondary Category'
                search
                selection
                options={secondaryOptions}
                value={selectedSecondary}
                onChange={handleSecondaryChange}
                disabled={!selectedPrimary}
                style={{ marginRight: '10px' }}
            />
            <Dropdown
                placeholder='Select Tertiary Category'
                search
                selection
                options={tertiaryOptions}
                value={selectedTertiary}
                onChange={handleTertiaryChange}
                disabled={!selectedSecondary}
                style={{ marginRight: '10px' }}
            />
        </div>
    );
};

export default DropdownExampleSearchSelectionTwo;