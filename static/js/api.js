// Usa `API_BASE_URL` definido en static/js/config.js (incluido en base.html antes de este archivo)
class ApiService {
    static getToken() {
        return localStorage.getItem('access_token');
    }

    static getRole() {
        return localStorage.getItem('user_role');
    }

    static setRole(role) {
        if (role) localStorage.setItem('user_role', role);
        else localStorage.removeItem('user_role');
    }

    static setToken(token) {
        if (token) localStorage.setItem('access_token', token);
        else localStorage.removeItem('access_token');
    }

    static async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const config = { ...options, headers };
        if (options.body && typeof options.body === 'object') config.body = JSON.stringify(options.body);

        const response = await fetch(url, config);

        if (response.status === 401) {
            // token invalid/expired — clear and redirect to login
            this.setToken(null);
            window.location.href = '/login';
            throw new Error('Unauthorized');
        }

        if (!response.ok) {
            let msg = `Error ${response.status}`;
            try {
                const data = await response.json();
                if (data && (data.message || data.msg)) msg = data.message || data.msg;
            } catch (e) {
                // ignore json parse errors
            }
            throw new Error(msg);
        }

        if (response.status === 204) return null;
        return response.json();
    }

    static get(entity) { return this.request(`/api/${entity}`); }
    static getById(entity, id) { return this.request(`/api/${entity}/${id}`); }
    static create(entity, data) { return this.request(`/api/${entity}`, { method: 'POST', body: data }); }
    static update(entity, id, data) { return this.request(`/api/${entity}/${id}`, { method: 'PUT', body: data }); }
    static delete(entity, id) { return this.request(`/api/${entity}/${id}`, { method: 'DELETE' }); }

    static async login(email, password) {
        const data = await this.request('/api/auth/login', { method: 'POST', body: { email, password } });
        if (data && data.access_token) this.setToken(data.access_token);
        // If backend returns role or user.role, persist it for frontend logic
        const role = data && (data.role || (data.user && data.user.role));
        if (role) this.setRole(role);
        return data;
    }

    static logout() { this.setToken(null); this.setRole(null); window.location.href = '/login'; }
}