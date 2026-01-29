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

/**
 * Get products with optional category filtering
 * @param {Object} filters - Optional category filters
 * @param {string} filters.primary_category - Primary category ID
 * @param {string} filters.secondary_category - Secondary category ID
 * @param {string} filters.tertiary_category - Tertiary category ID
 * @returns {Promise<Array>} Array of products
 */
export async function getProducts(filters = {}) {
    const params = new URLSearchParams();

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
    const endpoint = `/product${queryString ? `?${queryString}` : ''}`;

    return apiRequest(endpoint);
}

/**
 * Get all stores in hierarchical structure
 * @returns {Promise<Array>} Array of categories with nested subcategories
 */
export async function getStores() {
    return apiRequest('/stores');
}

/**
 * Get all categories in hierarchical structure
 * @returns {Promise<Array>} Array of categories with nested subcategories
 */
export async function getCategories() {
    return apiRequest('/categories');
}

/**
 * Get products by primary category only
 * @param {string} primaryCategory - Primary category ID
 * @returns {Promise<Array>} Array of products
 */
export async function getProductsByPrimaryCategory(primaryCategory) {
    return getProducts({ primary_category: primaryCategory });
}

/**
 * Get products by primary and secondary categories
 * @param {string} primaryCategory - Primary category ID
 * @param {string} secondaryCategory - Secondary category ID
 * @returns {Promise<Array>} Array of products
 */
export async function getProductsBySecondaryCategory(primaryCategory, secondaryCategory) {
    return getProducts({
        primary_category: primaryCategory,
        secondary_category: secondaryCategory
    });
}

/**
 * Get products by all three category levels
 * @param {string} primaryCategory - Primary category ID
 * @param {string} secondaryCategory - Secondary category ID
 * @param {string} tertiaryCategory - Tertiary category ID
 * @returns {Promise<Array>} Array of products
 */
export async function getProductsByTertiaryCategory(primaryCategory, secondaryCategory, tertiaryCategory) {
    return getProducts({
        primary_category: primaryCategory,
        secondary_category: secondaryCategory,
        tertiary_category: tertiaryCategory
    });
}