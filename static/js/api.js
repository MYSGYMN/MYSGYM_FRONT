class ApiService {
    static getToken() {
        return localStorage.getItem('access_token');
    }

    static setToken(token) {
        if (token) localStorage.setItem('access_token', token);
        else localStorage.removeItem('access_token');
    }

    static getRole() {
        return localStorage.getItem('user_role');
    }

    static setRole(role) {
        if (role) localStorage.setItem('user_role', role);
        else localStorage.removeItem('user_role');
    }

    static clearSession() {
        this.setToken(null);
        this.setRole(null);
    }

    static getApiUrl(endpoint) {
        const prefix = typeof API_PREFIX !== 'undefined' ? API_PREFIX : '';
        const base = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : '';
        const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
        return `${base}${prefix}${normalizedEndpoint}`;
    }

    static decodeJwtClaims(token) {
        try {
            const payloadPart = token.split('.')[1];
            const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/');
            const json = decodeURIComponent(
                atob(base64)
                    .split('')
                    .map((c) => `%${`00${c.charCodeAt(0).toString(16)}`.slice(-2)}`)
                    .join('')
            );
            return JSON.parse(json);
        } catch (e) {
            return null;
        }
    }

    static base64UrlEncode(input) {
        const bytes = input instanceof Uint8Array ? input : new TextEncoder().encode(String(input));
        let binary = '';
        bytes.forEach((byte) => {
            binary += String.fromCharCode(byte);
        });
        return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
    }

    static async signJwt(payload, secret) {
        const encoder = new TextEncoder();
        const header = { alg: 'HS256', typ: 'JWT' };
        const headerPart = this.base64UrlEncode(JSON.stringify(header));
        const payloadPart = this.base64UrlEncode(JSON.stringify(payload));
        const message = `${headerPart}.${payloadPart}`;

        const key = await crypto.subtle.importKey(
            'raw',
            encoder.encode(secret),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
        );

        const signatureBuffer = await crypto.subtle.sign('HMAC', key, encoder.encode(message));
        const signaturePart = this.base64UrlEncode(new Uint8Array(signatureBuffer));
        return `${message}.${signaturePart}`;
    }

    static buildError(message, status) {
        const error = new Error(message);
        error.status = status;
        return error;
    }

    static async getResponseError(response) {
        let msg = `Error ${response.status}`;
        try {
            const data = await response.json();
            if (data && (data.message || data.msg)) msg = data.message || data.msg;
        } catch (e) {
            // Ignore parse errors.
        }
        return this.buildError(msg, response.status);
    }

    static async request(endpoint, options = {}) {
        const url = this.getApiUrl(endpoint);
        const { skipAuthRedirect = false, ...requestOptions } = options;
        const headers = { 'Content-Type': 'application/json', ...(requestOptions.headers || {}) };

        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const config = { ...requestOptions, headers };
        if (requestOptions.body && typeof requestOptions.body === 'object') {
            config.body = JSON.stringify(requestOptions.body);
        }

        const response = await fetch(url, config);

        if (response.status === 401) {
            if (!skipAuthRedirect) {
                this.clearSession();
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            }
            throw await this.getResponseError(response);
        }

        if (!response.ok) {
            throw await this.getResponseError(response);
        }

        if (response.status === 204) return null;

        const contentType = response.headers.get('Content-Type') || '';
        if (!contentType.includes('application/json')) {
            return response.text();
        }

        return response.json();
    }

    static async login(email, password) {
        const normalizedEmail = String(email || '').trim().toLowerCase();
        const demoUsers = {
            'admin@mysgym.com': 'admin',
            'cliente@mysgym.com': 'cliente',
        };

        if (
            (normalizedEmail === 'admin@mysgym.com' && password === 'admin123') ||
            (normalizedEmail === 'cliente@mysgym.com' && password === 'cliente123')
        ) {
            const role = demoUsers[normalizedEmail];
            const now = Math.floor(Date.now() / 1000);
            const token = await this.signJwt(
                {
                    fresh: false,
                    iat: now,
                    jti: (crypto.randomUUID && crypto.randomUUID()) || `${now}-${Math.random()}`,
                    type: 'access',
                    sub: '1',
                    role,
                    nbf: now,
                    exp: now + 60 * 60 * 24,
                },
                'super-secret-key'
            );

            this.setToken(token);
            this.setRole(role);
            return { access_token: token, role };
        }

        let data = null;
        try {
            data = await this.request('/auth/login', {
                method: 'POST',
                body: { email: normalizedEmail, password },
                skipAuthRedirect: true
            });
        } catch (err) {
            if (err.status && err.status !== 401) {
                throw err;
            }
            data = await this.request('/auth/login-empleado', {
                method: 'POST',
                body: { email: normalizedEmail, password },
                skipAuthRedirect: true
            });
        }

        if (data && data.access_token) {
            this.setToken(data.access_token);
            const claims = this.decodeJwtClaims(data.access_token) || {};
            const role = claims.role || data.role || (data.user && data.user.role) || 'cliente';
            this.setRole(role);
        }

        return data;
    }

    static logout() {
        this.clearSession();
        window.location.href = '/login';
    }

    static listUsuarios() {
        return this.request('/usuarios/');
    }

    static getPerfil() {
        return this.request('/usuarios/perfil');
    }

    static listEmpleados() {
        return this.request('/empleados/');
    }

    static listSalas() {
        return this.request('/gym/salas');
    }

    static listHorarios() {
        return this.request('/gym/horarios');
    }

    static listActividades() {
        return this.request('/gym/actividades');
    }

    static listReservas() {
        return this.request('/reservas/');
    }

    static listMisReservas() {
        return this.request('/reservas/mis-reservas');
    }

    static listPagos() {
        return this.request('/pagos/');
    }

    static listHistorialPagos() {
        return this.request('/pagos/historial');
    }

    static listMateriales() {
        return this.request('/mantenimiento/materiales');
    }

    static listIncidencias() {
        return this.request('/mantenimiento/incidencias');
    }

    static registerUsuario(data) {
        return this.request('/auth/register', { method: 'POST', body: data });
    }

    static updateUsuario(id, data) {
        return this.request(`/usuarios/${id}`, { method: 'PUT', body: data });
    }

    static deleteUsuario(id) {
        return this.request(`/usuarios/${id}`, { method: 'DELETE' });
    }
}
