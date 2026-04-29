const runtimeConfig = window.MYSGYM_CONFIG || {};

function trimTrailingSlashes(value) {
    return String(value || '').replace(/\/+$/, '');
}

// El frontend llama directamente al backend via CORS
// Configura FRONTEND_API_BASE_URL en el .env para apuntar al backend
const API_BASE_URL = trimTrailingSlashes(runtimeConfig.apiBaseUrl);
const API_PREFIX = '';
const USE_MOCK_API = false;
