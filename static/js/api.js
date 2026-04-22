// Usa `API_BASE_URL` definido en static/js/config.js (incluido en base.html antes de este archivo)
class ApiService {
    // --- Mock helpers (solo cuando USE_MOCK_API=true en config.js) ---
    static ensureMockDb() {
        if (window.__mockDb) return window.__mockDb;
        // estructura simple en memoria para pruebas
        window.__mockDb = {
            usuarios: [
                { id_usuario: 1, nombre: 'Admin Demo', email: 'admin@local', password: 'admin', telefono: '600000001', fecha_registro: '2026-01-01', estado: 'activo', role: 'admin' },
                { id_usuario: 2, nombre: 'Empleado Demo', email: 'empleado@local', password: 'empleado', telefono: '600000002', fecha_registro: '2026-02-01', estado: 'activo', role: 'admin' },
                { id_usuario: 3, nombre: 'Cliente Demo', email: 'cliente@local', password: 'cliente', telefono: '600000003', fecha_registro: '2026-03-01', estado: 'activo', role: 'client' },
            ],
            nextId: 4,
        };
        return window.__mockDb;
    }

    static async mockRequest(endpoint, options = {}) {
        const db = this.ensureMockDb();
        const method = (options.method || 'GET').toUpperCase();
        // autenticación mock
        if (endpoint === '/api/auth/login' && method === 'POST') {
            const body = options.body || {};
            const email = body.email;
            const password = body.password;
            const user = db.usuarios.find(u => (u.email === email || u.email === (email || '')) && u.password === password);
            if (!user) {
                return Promise.reject(new Error('Credenciales inválidas (mock)'));
            }
            const token = 'mock-token-' + user.id_usuario;
            return Promise.resolve({ access_token: token, role: user.role, user: { id_usuario: user.id_usuario, nombre: user.nombre, email: user.email } });
        }

        // CRUD usuarios
        if (endpoint === '/api/usuarios') {
            if (method === 'GET') return Promise.resolve(db.usuarios.map(u => ({ ...u })));
            if (method === 'POST') {
                const body = options.body || {};
                const newRec = {
                    id_usuario: db.nextId++,
                    nombre: body.nombre || '',
                    email: body.email || '',
                    password: body.password || '',
                    telefono: body.telefono || '',
                    fecha_registro: body.fecha_registro || new Date().toISOString().slice(0,10),
                    estado: body.estado || 'activo',
                    role: body.role || 'client',
                };
                db.usuarios.push(newRec);
                return Promise.resolve(newRec);
            }
        }

        const matchId = endpoint.match(/^\/api\/usuarios\/(\d+)$/);
        if (matchId) {
            const id = parseInt(matchId[1], 10);
            const rec = db.usuarios.find(u => u.id_usuario === id);
            if (method === 'GET') return rec ? Promise.resolve({ ...rec }) : Promise.reject(new Error('No encontrado'));
            if (method === 'PUT') {
                if (!rec) return Promise.reject(new Error('No encontrado'));
                const body = options.body || {};
                Object.assign(rec, body);
                return Promise.resolve({ ...rec });
            }
            if (method === 'DELETE') {
                if (!rec) return Promise.reject(new Error('No encontrado'));
                db.usuarios = db.usuarios.filter(u => u.id_usuario !== id);
                return Promise.resolve(null);
            }
        }

        return Promise.reject(new Error('Endpoint mock no implementado: ' + endpoint));
    }

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
        // Si el modo mock está activado, manejar la petición en memoria
        if (typeof USE_MOCK_API !== 'undefined' && USE_MOCK_API) {
            // Al mockear, `options.body` ya viene como objeto desde los helpers
            try {
                return await this.mockRequest(endpoint, options);
            } catch (err) {
                // Mantener semántica de error como reject
                throw err;
            }
        }

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