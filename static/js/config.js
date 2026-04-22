// Configuración del frontend: URL base de la API (el backend debe ejecutarse aquí)
// Cambia este valor cuando ejecutes el backend en otro host/puerto o en producción.
// Por defecto durante desarrollo el servidor Flask corre en el puerto 8080.
const API_BASE_URL = "http://localhost:8080";

// Modo de desarrollo: si está activado, las llamadas a la API se simulan
// en el frontend con datos en memoria para poder hacer ensayos sin backend.
// Cambia a `false` para usar el backend real.
const USE_MOCK_API = true;
