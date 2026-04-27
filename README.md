# MYSGYM Frontend

Frontend Flask/Jinja para MYSGYM. Este proyecto sirve la interfaz web y se comunica con el backend REST via CORS.

## Resumen

- Servidor Flask para páginas HTML.
- Plantillas Jinja para `home`, `login`, `dashboard` y vistas de entidad.
- Cliente API en navegador que llama directamente al backend (CORS).
- Autenticación con JWT guardado en `localStorage`.
- Soporte para roles `cliente`, `admin` y `monitor`.

## Qué incluye

- [`app.py`](app.py): aplicación Flask principal, rutas y configuración.
- [`templates/base.html`](templates/base.html): layout común, navegación y lógica de permisos.
- [`templates/home.html`](templates/home.html): pantalla de resumen.
- [`templates/login.html`](templates/login.html): formulario de acceso.
- [`templates/dashboard.html`](templates/dashboard.html): panel de socios.
- [`templates/entity.html`](templates/entity.html): vista genérica para entidades.
- [`static/js/api.js`](static/js/api.js): cliente API con manejo de token, login y errores.
- [`static/js/config.js`](static/js/config.js): configuración de URLs.
- [`static/js/dashboard.js`](static/js/dashboard.js): lógica del panel de socios.
- [`static/js/entities.js`](static/js/entities.js): lógica CRUD de entidades.
- [`static/js/main.js`](static/js/main.js): utilidades generales de UI.
- [`static/css/styles.css`](static/css/styles.css): estilos globales.

## Arquitectura

```
Frontend:8080  ──────────────▶  Backend:8000
  HTML/JS        CORS         REST API
```

El frontend llama directamente al backend desde el navegador viaHTTPCORS.

## Rutas del frontend

- `/`: resumen principal.
- `/login`: pantalla de acceso.
- `/dashboard`: listado de socios.
- `/seccion/<entity>`: vista de entidad.

Entidades:

- `usuarios`
- `empleados`
- `salas`
- `horarios`
- `actividades`
- `reservas`
- `material`
- `incidencias`
- `pagos`

## Variables de entorno

- `FRONTEND_API_BASE_URL`
  - Valor por defecto: `http://localhost:8000`
  - URL del backend al que el navegador conecta directamente.

## Permisos en la UI

- `cliente`:
  - Perfil, Mis reservas, Mis pagos
  - acceso bloqueado a Resumen y Dashboard
- `admin`:
  - acceso completo a todas las entidades
- `monitor`:
  - acceso limitado similar a admin

## Requisitos

- Python 3.11+
- Flask
- Backend corriendo en `http://localhost:8000`

## Cómo ejecutar

1. Backend (terminal 1):
```bash
cd Backend_MYSGYM
source .venv/bin/activate
python run.py
```

2. Frontend (terminal 2):
```bash
cd MYSGYM_FRONT
source venv/bin/activate
python app.py
```

3. Navegador:
```
http://localhost:8080
```

## Estructura

```
MYSGYM_FRONT/
├── app.py
├── README.md
├── static/
│   ├── css/
│   └── js/
└── templates/
```