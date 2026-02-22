// API service for communicating with the backend
const API_BASE_URL = '/api';

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
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
    return apiRequest('/stores');
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