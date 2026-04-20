/**
 * API Service for External Database Communication
 * This module handles all requests to the external backend/database.
 */

class ApiService {
    constructor(baseUrl = 'https://api.tuservidor.com/v1') {
        this.baseUrl = baseUrl;
        this.isConnected = false;
    }

    /**
     * Simulates a connection check to the external database
     */
    async checkConnection() {
        // En un entorno real, aquí harías un fetch a un endpoint de salud/ping
        return new Promise((resolve) => {
            setTimeout(() => {
                this.isConnected = true;
                resolve({ success: true, message: 'Conectado a la base de datos externa' });
            }, 1500);
        });
    }

    /**
     * Example method to fetch data from a table/collection
     */
    async getData(endpoint) {
        if (!this.isConnected) {
            console.warn('Intentando obtener datos sin conexión activa.');
        }

        try {
            // Ejemplo de fetch real (comentado para evitar errores de red en el demo)
            /*
            const response = await fetch(`${this.baseUrl}/${endpoint}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
            */

            // Simulación de respuesta exitosa
            return [
                { id: 1, name: 'Rutina de Volumen', status: 'Active' },
                { id: 2, name: 'Dieta Keto Pro', status: 'Draft' },
                { id: 3, name: 'Entrenamiento HIIT', status: 'Active' }
            ];
        } catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    }
}

// Exportar instancia única
const api = new ApiService();
