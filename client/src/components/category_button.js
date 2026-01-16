import React, { useState, useEffect } from 'react';
import { Dropdown } from 'semantic-ui-react';
import { getCategories } from '../services/api';

const Categories = ({ onCategoryChange }) => {
    const [categories, setCategories] = useState({
        primary: [],
        secondary: {},
        tertiary: {}
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedPrimary, setSelectedPrimary] = useState('');
    const [selectedSecondary, setSelectedSecondary] = useState('');
    const [selectedTertiary, setSelectedTertiary] = useState('');

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                setLoading(true);
                const categoryData = await getCategories();

                // Transform hierarchical data to flat structure for the component
                const transformedCategories = {
                    primary: [],
                    secondary: {},
                    tertiary: {}
                };

                categoryData.forEach(primaryCat => {
                    // Add primary category
                    transformedCategories.primary.push({
                        key: primaryCat.id,
                        text: primaryCat.name,
                        value: primaryCat.id
                    });

                    // Process secondary categories
                    if (primaryCat.subcategories) {
                        primaryCat.subcategories.forEach(secondaryCat => {
                            // Add secondary category under primary
                            if (!transformedCategories.secondary[primaryCat.id]) {
                                transformedCategories.secondary[primaryCat.id] = [];
                            }
                            transformedCategories.secondary[primaryCat.id].push({
                                key: secondaryCat.id,
                                text: secondaryCat.name,
                                value: secondaryCat.id
                            });

                            // Process tertiary categories
                            if (secondaryCat.subcategories) {
                                secondaryCat.subcategories.forEach(tertiaryCat => {
                                    // Add tertiary category under secondary
                                    if (!transformedCategories.tertiary[secondaryCat.id]) {
                                        transformedCategories.tertiary[secondaryCat.id] = [];
                                    }
                                    transformedCategories.tertiary[secondaryCat.id].push({
                                        key: tertiaryCat.id,
                                        text: tertiaryCat.name,
                                        value: tertiaryCat.id
                                    });
                                });
                            }
                        });
                    }
                });

                setCategories(transformedCategories);
                setError(null);
            } catch (err) {
                console.error('Error fetching categories:', err);
                setError('Failed to load categories');
            } finally {
                setLoading(false);
            }
        };

        fetchCategories();
    }, []);

    const handlePrimaryChange = (e, { value }) => {
        const newCategories = {
            primary: value,
            secondary: '',
            tertiary: ''
        };
        setSelectedPrimary(value);
        setSelectedSecondary('');
        setSelectedTertiary('');
        onCategoryChange && onCategoryChange(newCategories);
    };

    const handleSecondaryChange = (e, { value }) => {
        const newCategories = {
            primary: selectedPrimary,
            secondary: value,
            tertiary: ''
        };
        setSelectedSecondary(value);
        setSelectedTertiary('');
        onCategoryChange && onCategoryChange(newCategories);
    };

    const handleTertiaryChange = (e, { value }) => {
        const newCategories = {
            primary: selectedPrimary,
            secondary: selectedSecondary,
            tertiary: value
        };
        setSelectedTertiary(value);
        onCategoryChange && onCategoryChange(newCategories);
    };

    const secondaryOptions = selectedPrimary ? categories.secondary[selectedPrimary] || [] : [];
    const tertiaryOptions = selectedSecondary ? categories.tertiary[selectedSecondary] || [] : [];

    if (loading) {
        return <div>Loading categories...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

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

export default Categories;