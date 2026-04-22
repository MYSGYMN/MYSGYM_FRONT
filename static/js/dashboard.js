document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('socios-table-body');
    const employeePanel = document.getElementById('employee-panel');
    const employeeTbody = document.getElementById('employee-table-body');
    const modal = document.getElementById('modal');
    const modalForm = document.getElementById('modal-form');
    const modalTitle = document.getElementById('modal-title');
    const btnNew = document.getElementById('btn-new');
    const btnLogout = document.getElementById('btn-logout');

    if (btnLogout) btnLogout.addEventListener('click', () => ApiService.logout());

    btnNew.addEventListener('click', () => openModal());

    document.getElementById('modal-cancel').addEventListener('click', closeModal);

    modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const id = form.id_usuario.value;
        const payload = {
            nombre: form.nombre.value.trim(),
            email: form.email.value.trim(),
            password: form.password.value,
            telefono: form.telefono.value.trim(),
            fecha_registro: form.fecha_registro.value,
            estado: form.estado.value.trim(),
        };

        try {
            if (id) {
                await ApiService.update('usuarios', id, payload);
            } else {
                await ApiService.create('usuarios', payload);
            }
            closeModal();
            await load();
        } catch (err) {
            alert(err.message || 'Error');
        }
    });

    async function load() {
        // Decide qué panel mostrar según el role
        const role = ApiService.getRole();
        if (!role) {
            // If role not present, try to fetch profile (optional)
        }

        if (role && (role.toLowerCase() === 'empleado' || role.toLowerCase() === 'employee')) {
            // show employee panel (read-only)
            if (employeePanel) employeePanel.style.display = '';
            if (tbody) tbody.closest('section').style.display = 'none';
            employeeTbody.innerHTML = '<tr><td colspan="4">Cargando...</td></tr>';
            try {
                const items = await ApiService.get('usuarios');
                renderEmployee(items);
            } catch (err) {
                employeeTbody.innerHTML = `<tr><td colspan="4">${err.message}</td></tr>`;
            }
            return;
        }

        // default: admin panel
        if (employeePanel) employeePanel.style.display = 'none';
        if (tbody) tbody.closest('section').style.display = '';
        tbody.innerHTML = '<tr><td colspan="7">Cargando...</td></tr>';
        try {
            const items = await ApiService.get('usuarios');
            render(items);
        } catch (err) {
            tbody.innerHTML = `<tr><td colspan="7">${err.message}</td></tr>`;
        }
    }

    function renderEmployee(items) {
        if (!items || items.length === 0) {
            employeeTbody.innerHTML = '<tr><td colspan="4">No hay registros</td></tr>';
            return;
        }
        employeeTbody.innerHTML = '';
        items.forEach((it) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${it.id_usuario ?? ''}</td>
                <td>${it.nombre ?? ''}</td>
                <td>${it.email ?? ''}</td>
                <td>${it.telefono ?? ''}</td>
            `;
            employeeTbody.appendChild(tr);
        });
    }

    function render(items) {
        if (!items || items.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No hay registros</td></tr>';
            return;
        }
        tbody.innerHTML = '';
        items.forEach((it) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${it.id_usuario ?? ''}</td>
                <td>${it.nombre ?? ''}</td>
                <td>${it.email ?? ''}</td>
                <td>${it.telefono ?? ''}</td>
                <td>${it.fecha_registro ?? ''}</td>
                <td>${it.estado ?? ''}</td>
                <td>
                    <button class="btn-link btn-edit" data-id="${it.id_usuario}">Editar</button>
                    <button class="btn-link btn-delete" data-id="${it.id_usuario}">Borrar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        document.querySelectorAll('.btn-edit').forEach((btn) => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                try {
                    const record = await ApiService.getById('usuarios', id);
                    openModal(record);
                } catch (err) {
                    alert(err.message || 'Error al cargar registro');
                }
            });
        });

        document.querySelectorAll('.btn-delete').forEach((btn) => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                if (!confirm('¿Borrar registro?')) return;
                try {
                    await ApiService.delete('usuarios', id);
                    await load();
                } catch (err) {
                    alert(err.message || 'Error al borrar');
                }
            });
        });
    }

    function openModal(record = null) {
        modalForm.reset();
        modalForm.id_usuario.value = record ? record.id_usuario : '';
        modalForm.nombre.value = record ? record.nombre : '';
        modalForm.email.value = record ? record.email : '';
        modalForm.password.value = '';
        modalForm.telefono.value = record ? record.telefono : '';
        modalForm.fecha_registro.value = record ? record.fecha_registro : '';
        modalForm.estado.value = record ? record.estado : '';
        modalTitle.textContent = record ? `Editar: ${record.nombre}` : 'Nuevo socio';
        modal.style.display = 'flex';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    // inicializar
    load();
});
