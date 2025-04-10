function getApiBaseUrl() {
    if (window.location.hostname.includes('csb.app')) {
        // For CodeSandbox environment
        const subdomain = window.location.hostname.split('.')[0];
        const baseSubdomain = subdomain.split('-')[0];
        return `https://${baseSubdomain}-8001.csb.app`;
    }
    // For local development
    return 'http://localhost:8001';
}

const API_BASE_URL = getApiBaseUrl();

export const API_URLS = {
    login: `${API_BASE_URL}/api/auth/login/`,
    register: `${API_BASE_URL}/api/auth/register/`,
    logout: `${API_BASE_URL}/api/auth/logout/`,
    profile: `${API_BASE_URL}/api/profile/`,
    codes: `${API_BASE_URL}/api/codes/`,
    transactions: `${API_BASE_URL}/api/transactions/`
};
