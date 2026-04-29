document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('socios-table-body');
    const clientPanel = document.getElementById('client-panel');
    const clientTbody = document.getElementById('client-table-body');
    const modal = document.getElementById('modal');
    const modalForm = document.getElementById('modal-form');
    const modalTitle = document.getElementById('modal-title');
    const btnNew = document.getElementById('btn-new');
    const btnLogout = document.getElementById('btn-logout');
    let permissions = {
        canEdit: false,
        canDelete: false,
    };

    if (btnLogout) btnLogout.addEventListener('click', () => ApiService.logout());

    if (btnNew) btnNew.addEventListener('click', () => openModal());

    document.getElementById('modal-cancel').addEventListener('click', closeModal);

    modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = e.target;
        const id = form.id_usuario.value;
        const payload = id
            ? {
                nombre: form.nombre.value.trim(),
                telefono: form.telefono.value.trim(),
                estado: form.estado.value.trim(),
            }
            : {
                nombre: form.nombre.value.trim(),
                email: form.email.value.trim(),
                password: form.password.value,
                telefono: form.telefono.value.trim(),
            };

        try {
            if (id) {
                await ApiService.updateUsuario(id, payload);
            } else {
                await ApiService.registerUsuario(payload);
            }
            closeModal();
            await load();
        } catch (err) {
            alert(err.message || 'Error');
        }
    });

    async function load() {
        const role = ApiService.getRole();
        if (!role) {
            // Si no hay `role`, intentar obtener el perfil (opcional)
        }

        if (isCliente) {
            if (clientPanel) clientPanel.style.display = '';
            if (tbody) tbody.closest('section').style.display = 'none';
            if (btnNew) btnNew.style.display = 'none';
            clientTbody.innerHTML = '<tr><td colspan="6">Cargando...</td></tr>';
            try {
                const perfil = await ApiService.getPerfil();
                renderClient([perfil]);
            } catch (err) {
                clientTbody.innerHTML = `<tr><td colspan="6">${err.message}</td></tr>`;
            }
            return;
        }

        if (!isStaff) {
            if (clientPanel) clientPanel.style.display = 'none';
            if (tbody) tbody.closest('section').style.display = '';
            if (btnNew) btnNew.style.display = 'none';
            tbody.innerHTML = '<tr><td colspan="7">No tienes acceso a este panel.</td></tr>';
            return;
        }

        if (clientPanel) clientPanel.style.display = 'none';
        if (tbody) tbody.closest('section').style.display = '';
        if (btnNew) btnNew.style.display = '';
        tbody.innerHTML = '<tr><td colspan="7">Cargando...</td></tr>';
        try {
            const items = await ApiService.listUsuarios();
            render(items);
        } catch (err) {
            tbody.innerHTML = `<tr><td colspan="7">${err.message}</td></tr>`;
        }
    }

    function renderClient(items) {
        if (!items || items.length === 0) {
            clientTbody.innerHTML = '<tr><td colspan="6">No hay registros</td></tr>';
            return;
        }
        clientTbody.innerHTML = '';
        items.forEach((it) => {
            // mostrar solo información básica para clientes
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${it.id_usuario ?? ''}</td>
                <td>${it.nombre ?? ''}</td>
                <td>${it.email ?? ''}</td>
                <td>${it.telefono ?? ''}</td>
                <td>${it.estado ?? ''}</td>
                <td>${it.fecha_registro ?? ''}</td>
            `;
            clientTbody.appendChild(tr);
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
            const actions = [];
            if (permissions.canEdit) {
                actions.push(`<button class="btn-link btn-edit" data-id="${it.id_usuario}">Editar</button>`);
            }
            if (permissions.canDelete) {
                actions.push(`<button class="btn-link btn-delete" data-id="${it.id_usuario}">Borrar</button>`);
            }
            tr.innerHTML = `
                <td>${it.id_usuario ?? ''}</td>
                <td>${it.nombre ?? ''}</td>
                <td>${it.email ?? ''}</td>
                <td>${it.telefono ?? ''}</td>
                <td>${it.estado ?? ''}</td>
                <td>${it.fecha_registro ?? ''}</td>
                <td>${actions.join(' ')}</td>
            `;
            tbody.appendChild(tr);
        });

        document.querySelectorAll('.btn-edit').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const id = Number(e.target.dataset.id);
                const record = items.find((x) => Number(x.id_usuario) === id);
                openModal(record || null);
            });
        });

        document.querySelectorAll('.btn-delete').forEach((btn) => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.dataset.id;
                if (!confirm('¿Borrar registro?')) return;
                try {
                    await ApiService.deleteUsuario(id);
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
        modalForm.estado.value = record ? record.estado : '';
        modalForm.email.disabled = Boolean(record);
        modalForm.password.disabled = Boolean(record);
        modalForm.estado.disabled = !record;
        modalForm.estado.parentElement.style.display = record ? '' : 'none';
        modalTitle.textContent = record ? `Editar: ${record.nombre}` : 'Nuevo socio';
        modal.style.display = 'flex';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    // inicializar
    load();
});
