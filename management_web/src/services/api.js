import { fetchAuthSession } from 'aws-amplify/auth';

// API service for communicating with the backend
const API_BASE_URL = '/api';

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest(endpoint, options = {}) {
    try {
        const session = await fetchAuthSession();
        const token = session.tokens.idToken.toString();
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                ...options.headers,
            },
            ...options,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(`API request failed for ${endpoint}:`, error);
        throw error;
    }
}

export async function getQuantities(storeId, productIds) {
    const idsString = productIds.join(',');

    const params = new URLSearchParams();
    params.append('store_id', storeId);
    params.append('product_ids', idsString);

    const endpoint = `/quantities?${params.toString()}`;
    return apiRequest(endpoint);
}

/**
 * Get products with optional category filtering
 * @param {Object} filters - Optional category filters
 * @param {string} filters.store - store ID
 * @param {string} filters.primary_category - Primary category ID
 * @param {string} filters.secondary_category - Secondary category ID
 * @param {string} filters.tertiary_category - Tertiary category ID
 * @returns {Promise<Array>} Array of products
 */
export async function getProducts(filters = {}) {
    const params = new URLSearchParams();

    if (filters.store) {
        params.append('store_id', filters.store);
    }
    if (filters.primary_category) {
        params.append('primary_category', filters.primary_category);
    }
    if (filters.secondary_category) {
        params.append('secondary_category', filters.secondary_category);
    }
    if (filters.tertiary_category) {
        params.append('tertiary_category', filters.tertiary_category);
    }

    const queryString = params.toString();
    const endpoint = `/products${queryString ? `?${queryString}` : ''}`;

    return apiRequest(endpoint);
}

/**
 * Get all stores in hierarchical structure
 * @returns {Promise<Array>} Array of categories with nested subcategories
 */
export async function getStores() {
    try {
        const endpoint = `/stores`;
        const storeData = await apiRequest(endpoint)
        const transformed = storeData.map(s => ({
            key: s.id,
            text: s.name,
            value: s.id
        }));
        return transformed
    } catch (err) {
        console.error(err);
        return [];
    }
}

export async function getCategories() {
    try {
        const endpoint = `/categories`;
        const categoryData = await apiRequest(endpoint)

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
        return transformedCategories;
    } catch (err) {
        console.error(err);
        return { primary: [], secondary: {}, tertiary: {} };
    }
}

export async function getUnofferedProducts(storeId) {
    const params = new URLSearchParams();
    params.append('store_id', storeId);

    const endpoint = `/unoffered-products?${params.toString()}`;
    return apiRequest(endpoint);
}

export async function offerProducts(storeId, newOffer) {
    return apiRequest('/products', {
        method: 'POST',
        body: JSON.stringify({ store_id: storeId, new_offer: newOffer }),
    });
}

export async function unofferProducts(storeId, productIds) {
    return apiRequest('/products', {
        method: 'DELETE',
        body: JSON.stringify({ store_id: storeId, product_ids: productIds }),
    });
}

export async function updateQuantity(storeId, update_items) {
    return apiRequest('/quantities', {
        method: 'PUT',
        body: JSON.stringify({ store_id: storeId, update_items }),
    });
}

export async function subscribe(storeId, categoryId, frequency) {
    var target_type = storeId ? 'store' : 'category';
    var target_id = storeId || categoryId;
    return apiRequest('/subscribe', {
        method: 'POST',
        body: JSON.stringify({ target_type, target_id, frequency }),
    });
}

export async function get_subscription() {
    return apiRequest('/subscriptions', {
        method: 'GET',
    });
}

export async function get_reports(taskId, page, PAGE_SIZE) {
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('page_size', PAGE_SIZE);

    return apiRequest(`/report/${taskId}/files?${params.toString()}`, {
        method: 'GET',
    });
}

export async function toggle_subscription_status(taskId, status) {
    return apiRequest(`/subscriptions/${taskId}/toggle`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
    });
}

export async function unsubscribe(taskId) {
    return apiRequest(`/subscriptions/${taskId}`, {
        method: 'DELETE',
    });
}