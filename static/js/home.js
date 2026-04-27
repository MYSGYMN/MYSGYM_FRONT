document.addEventListener('DOMContentLoaded', () => {
    const role = String(ApiService.getRole() || '').toLowerCase();
    const isStaff = role === 'admin' || role === 'monitor';

    const kpiEntities = document.getElementById('home-kpi-entities');
    const kpiRecords = document.getElementById('home-kpi-records');
    const kpiUsers = document.getElementById('home-kpi-users');
    const kpiRelations = document.getElementById('home-kpi-relations');
    const kpiRevenue = document.getElementById('home-kpi-revenue');
    const kpiIssues = document.getElementById('home-kpi-issues');
    const paymentsBody = document.getElementById('home-payments-body');
    const distribution = document.getElementById('home-distribution');

    const sections = [
        { key: 'usuarios', label: 'Usuarios', loader: () => (isStaff ? ApiService.listUsuarios() : ApiService.getPerfil()) },
        { key: 'empleados', label: 'Empleados', loader: () => (isStaff ? ApiService.listEmpleados() : []) },
        { key: 'salas', label: 'Salas', loader: () => ApiService.listSalas() },
        { key: 'horarios', label: 'Horarios', loader: () => ApiService.listHorarios() },
        { key: 'actividades', label: 'Actividades', loader: () => ApiService.listActividades() },
        { key: 'reservas', label: 'Reservas', loader: () => (isStaff ? ApiService.listReservas() : ApiService.listMisReservas()) },
        { key: 'material', label: 'Material', loader: () => (isStaff ? ApiService.listMateriales() : []) },
        { key: 'incidencias', label: 'Incidencias', loader: () => (isStaff ? ApiService.listIncidencias() : []) },
        { key: 'pagos', label: 'Pagos', loader: () => (isStaff ? ApiService.listPagos() : ApiService.listHistorialPagos()) },
    ];

    const fetchers = sections.map(async (section) => {
        try {
            const data = await section.loader();
            return { ...section, data: normalizeArray(data) };
        } catch (error) {
            return { ...section, data: [], error };
        }
    });

    Promise.all(fetchers).then((results) => {
        const counts = Object.fromEntries(results.map((result) => [result.key, result.data.length]));
        const totalRecords = Object.values(counts).reduce((sum, value) => sum + value, 0);
        const totalUsers = results.find((result) => result.key === 'usuarios');
        const payments = results.find((result) => result.key === 'pagos')?.data || [];
        const reservations = results.find((result) => result.key === 'reservas')?.data || [];
        const activities = results.find((result) => result.key === 'actividades')?.data || [];
        const issues = results.find((result) => result.key === 'incidencias')?.data || [];
        const materials = results.find((result) => result.key === 'material')?.data || [];

        if (kpiEntities) kpiEntities.textContent = String(sections.length);
        if (kpiRecords) kpiRecords.textContent = String(totalRecords);
        if (kpiRelations) {
            kpiRelations.textContent = String(activities.length + reservations.length + payments.length + materials.length + issues.length);
        }

        if (kpiUsers) {
            if (isStaff) {
                const activeUsers = (totalUsers?.data || []).filter((user) => normalizeStatus(user.estado) === 'activo').length;
                kpiUsers.textContent = `${activeUsers} usuario${activeUsers === 1 ? '' : 's'} activo${activeUsers === 1 ? '' : 's'}`;
            } else {
                const perfil = totalUsers?.data?.[0] || null;
                const active = perfil && normalizeStatus(perfil.estado) === 'activo' ? 1 : 0;
                kpiUsers.textContent = `${active} usuario${active === 1 ? '' : 's'} activo${active === 1 ? '' : 's'}`;
            }
        }

        const totalRevenue = payments.reduce((sum, payment) => sum + Number(payment.monto || 0), 0);
        if (kpiRevenue) kpiRevenue.innerHTML = `${totalRevenue.toFixed(2)}<span class="kpi-unit">€</span>`;

        const openIssues = issues.filter((issue) => normalizeStatus(issue.estado) === 'pendiente').length;
        if (kpiIssues) {
            kpiIssues.textContent = `${openIssues} incidencia${openIssues === 1 ? '' : 's'} abierta${openIssues === 1 ? '' : 's'}`;
        }

        renderPayments(payments);
        renderDistribution(results);
    });

    function renderPayments(payments) {
        if (!paymentsBody) return;

        const sorted = [...payments]
            .sort((a, b) => new Date(b.fecha || 0).getTime() - new Date(a.fecha || 0).getTime())
            .slice(0, 5);

        if (!sorted.length) {
            paymentsBody.innerHTML = '<tr><td colspan="4">No hay pagos registrados.</td></tr>';
            return;
        }

        paymentsBody.innerHTML = '';
        sorted.forEach((payment) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${escapeHtml(payment.id_pago ?? '')}</td>
                <td>${escapeHtml(payment.usuario ?? payment.usuario_nombre ?? '—')}</td>
                <td>${escapeHtml(formatMoney(payment.monto ?? 0))}</td>
                <td>${escapeHtml(payment.metodo ?? payment.metodo_pago ?? '—')}</td>
            `;
            paymentsBody.appendChild(tr);
        });
    }

    function renderDistribution(results) {
        if (!distribution) return;

        const rows = results
            .map((result) => ({ label: result.label, count: result.data.length }))
            .filter((row) => row.count > 0)
            .sort((a, b) => b.count - a.count);

        if (!rows.length) {
            distribution.innerHTML = '<div class="bar-row"><span class="bar-name">Sin datos</span><div class="bar-track"><div class="bar-fill" style="width: 0;"></div></div><span class="bar-val">0</span></div>';
            return;
        }

        const max = Math.max(...rows.map((row) => row.count));
        distribution.innerHTML = rows
            .map((row) => {
                const width = Math.max(8, Math.round((row.count / max) * 100));
                return `
                    <div class="bar-row">
                        <span class="bar-name">${escapeHtml(row.label)}</span>
                        <div class="bar-track"><div class="bar-fill" style="width: ${width}%"></div></div>
                        <span class="bar-val">${row.count}</span>
                    </div>
                `;
            })
            .join('');
    }

    function normalizeArray(data) {
        if (Array.isArray(data)) return data;
        if (data && typeof data === 'object') return [data];
        return [];
    }

    function normalizeStatus(value) {
        const normalized = String(value || '').toLowerCase();
        if (['activo', 'activa', 'confirmada', 'completado', 'completada', 'cobrado', 'operativo'].includes(normalized)) {
            return 'activo';
        }
        if (['pendiente', 'revision', 'en espera', 'abierto', 'abierta'].includes(normalized)) {
            return 'pendiente';
        }
        return 'inactivo';
    }

    function formatMoney(value) {
        const number = Number(value);
        if (Number.isNaN(number)) return String(value);
        return `${number.toFixed(2)} €`;
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }
});
