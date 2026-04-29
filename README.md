# MYSGYM Frontend

Frontend ligero para la aplicación MYSGYM: una interfaz basada en Flask que sirve plantillas Jinja y recursos estáticos (CSS/JS). Está pensado como capa de presentación que puede trabajar con un backend REST separado o usar el modo mock-interno para desarrollo.

Última actualización: 28 de abril de 2026

## Propósito

Proveer una interfaz web para gestionar entidades del gimnasio (usuarios, empleados, salas, actividades, reservas, material, incidencias y pagos). Incluye:

- Plantillas HTML con estructura base y zonas donde el cliente JS carga datos.
- Servicios JavaScript para consumir una API (con soporte a JWT y modo mock para pruebas locales).
- Un servidor Flask mínimo que sirve las plantillas y proporciona endpoints de prueba (dev) cuando se necesita.

## Tecnologías principales

- Python + Flask (servidor que sirve las plantillas y algunos endpoints de prueba).
- HTML + Jinja2 (plantillas en `templates/`).
- JavaScript (cliente en `static/js/`): `ApiService` (peticiones, autenticación), `dashboard.js` (lógica de listado/CRUD de ejemplo), `main.js` (comportamientos UI).
- CSS en `static/css/styles.css`.

## Estructura principal

```
MYSGYM_FRONT/
├── app.py                 # Servidor Flask (dev)
├── templates/             # Plantillas Jinja: base.html, home.html, dashboard.html, entity.html, login.html
├── static/
│   ├── css/
│   └── js/
│       ├── config.js     # API_BASE_URL, USE_MOCK_API
│       ├── api.js        # ApiService (mock + fetch, JWT storage)
│       ├── dashboard.js  # Lógica de listado/CRUD de ejemplo
│       └── main.js       # Comportamientos UI comunes
└── README.md
```

## Cómo ejecutar (desarrollo)

1. Crear y activar un entorno virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar Flask:

```bash
pip install flask
```

3. Ejecutar la aplicación de desarrollo (sirve en el puerto 8080 por defecto):

```bash
python app.py
```

4. Abrir en el navegador: http://localhost:8080

## Configuración importante

- `static/js/config.js`:
	- `API_BASE_URL`: URL base del backend. Por defecto `http://localhost:8080` (el mismo servidor Flask de este proyecto).
	- `USE_MOCK_API`: si `true`, `ApiService` usa un mock en memoria para pruebas sin backend; poner `false` para realizar peticiones reales al `API_BASE_URL`.

## Endpoints útiles (frontend + dev API)

- Páginas:
	- `/` → `home` (plantilla `home.html`)
	- `/dashboard` → panel principal (`dashboard.html`)
	- `/login` → formulario de acceso (`login.html`)
	- `/seccion/<entity>` → vista genérica por entidad (`entity.html`)

- API de prueba (dev):
	- `POST /api/auth/login` → autenticación de desarrollo (dev tokens)
	- `GET/POST /api/usuarios` y `GET/PUT/DELETE /api/usuarios/<id>` → ejemplo CRUD para `usuarios`

El servidor `app.py` incluye una base de datos en memoria y endpoints simples para facilitar pruebas locales.

## Credenciales de prueba

- Usuario admin de ejemplo: `admin` / `admin` (dev)
- Usuario empleado de ejemplo: `empleado` / `empleado` (dev)

Además, cuando `USE_MOCK_API=true` el cliente contiene usuarios demo en memoria (ver `static/js/api.js`).

## Uso básico del frontend

1. Si quieres usar el backend incluido para pruebas: mantener `API_BASE_URL` en `http://localhost:8080` y `USE_MOCK_API=false`.
2. Abrir `/login`, iniciar sesión con credenciales de prueba.
3. Navegar al `/dashboard` para listar y gestionar usuarios (CRUD de ejemplo).
4. Para cambiar a un backend externo, actualizar `static/js/config.js` con la URL del API y poner `USE_MOCK_API = false`.

## Notas y siguientes pasos sugeridos

- Separar el backend real si se requiere persistencia en base de datos.
- Extender `ApiService` con manejo de refresh tokens y control de errores más robusto.
- Añadir tests E2E y scripts de despliegue cuando el backend esté disponible.



