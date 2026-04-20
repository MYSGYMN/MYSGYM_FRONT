/**
 * Main Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const btnConnect = document.getElementById('btn-connect');
    const statusDot = document.getElementById('status-dot');
    const statusText = document.getElementById('status-text');
    const dataDisplay = document.getElementById('data-display');

    // Inicialización
    console.log('MYSGYM Frontend Initialized');

    // Event Listeners
    btnConnect.addEventListener('click', async () => {
        // Actualizar UI a estado de carga
        btnConnect.disabled = true;
        btnConnect.textContent = 'Conectando...';
        statusText.textContent = 'Intentando conectar...';

        try {
            // Llamada al servicio API (simulado en api.js)
            const response = await api.checkConnection();

            if (response.success) {
                // Actualizar indicadores de estado
                statusDot.classList.remove('dot-red');
                statusDot.classList.add('dot-green');
                statusText.textContent = 'Conectado';
                btnConnect.textContent = 'Refrescar Datos';
                btnConnect.disabled = false;

                // Cargar datos de ejemplo
                loadDashboardData();
            }
        } catch (error) {
            console.error('Connection failed:', error);
            statusText.textContent = 'Error de conexión';
            btnConnect.disabled = false;
            btnConnect.textContent = 'Reintentar';
        }
    });

    /**
     * Carga y renderiza datos en el dashboard
     */
    async function loadDashboardData() {
        // Mostrar skeletons (ya están por defecto, pero podríamos reiniciarlos)
        dataDisplay.innerHTML = '';
        for(let i=0; i<3; i++) {
            dataDisplay.innerHTML += `
                <div class="card skeleton">
                    <div class="skeleton-line"></div>
                    <div class="skeleton-line short"></div>
                </div>
            `;
        }

        const data = await api.getData('dashboard');

        // Simular un pequeño retraso de carga para ver la animación
        setTimeout(() => {
            renderCards(data);
        }, 1000);
    }

    /**
     * Renderiza las tarjetas de datos
     */
    function renderCards(items) {
        dataDisplay.innerHTML = ''; // Limpiar skeletons
        
        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3 style="color: var(--accent); margin-bottom: 0.5rem;">${item.name}</h3>
                <p style="color: var(--text-muted); font-size: 0.9rem;">ID de base de datos: #${item.id}</p>
                <div style="margin-top: 1rem;">
                    <span style="background: ${item.status === 'Active' ? '#10b98133' : '#f59e0b33'}; 
                                 color: ${item.status === 'Active' ? '#10b981' : '#f59e0b'}; 
                                 padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.8rem; font-weight: 700;">
                        ${item.status}
                    </span>
                </div>
            `;
            dataDisplay.appendChild(card);
        });
    }
});
