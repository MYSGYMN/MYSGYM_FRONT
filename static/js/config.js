// Configuración del frontend: URL base de la API.
// El frontend Flask sirve las páginas y el backend separado responde a las rutas REST.
const API_BASE_URL = `http://${window.location.hostname}:8000`;

// Modo de desarrollo: si está activado, las llamadas a la API se simulan
// en el frontend con datos en memoria para poder hacer ensayos sin backend.
// Cambia a `false` para usar el backend real.
const USE_MOCK_API = false;
