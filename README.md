# MYSGYM — Frontend (Flask + Jinja)

Frontend ligero para la aplicación MYSGYM: una interfaz basada en Flask que sirve plantillas Jinja y recursos estáticos (CSS/JS). La persistencia y la autenticación viven en un backend REST separado.

Última actualización: 28 de abril de 2026

## Propósito

Proveer una interfaz web para gestionar entidades del gimnasio (usuarios, empleados, salas, actividades, reservas, material, incidencias y pagos). Incluye:

- Plantillas HTML con estructura base y zonas donde el cliente JS carga datos.
- Servicios JavaScript para consumir una API (con soporte a JWT y modo mock para pruebas locales).
- Un servidor Flask mínimo que solo sirve las plantillas y los recursos estáticos.

## Tecnologías principales

- Python + Flask (servidor que sirve las plantillas).
- HTML + Jinja2 (plantillas en `templates/`).
- JavaScript (cliente en `static/js/`): `ApiService` (peticiones, autenticación), `dashboard.js` (lógica de listado/CRUD de ejemplo), `main.js` (comportamientos UI).
- CSS en `static/css/styles.css`.

## Estructura principal

```
MYSGYM_FRONT/
├── app.py                 # Servidor Flask (dev)
├── templates/             # Plantillas Jinja: base.html, home.html, dashboard.html, entity.html, login.html
├── static/
│   ├── css/styles.css
│   └── js/
│       ├── config.js     # API_BASE_URL, USE_MOCK_API
│       ├── api.js        # ApiService (fetch, JWT storage y mock opcional)
│       ├── home.js       # Carga KPIs y resumen desde el backend
│       ├── entity.js     # CRUD genérico de entidades desde el backend
│       ├── dashboard.js  # Lógica de listado/CRUD de usuarios
│       └── main.js       # Comportamientos UI comunes
└── README.md
```

## Cómo hacer funcionar el proyecto (Paso a paso)

Sigue estos pasos exactos para configurar el entorno y arrancar la aplicación en un PC nuevo:

### 1. Preparar el entorno virtual
Crea un entorno de Python para aislar las librerías del sistema:
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- **En Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
- **En Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 3. Instalar las dependencias
Instala Flask, Pytest y el resto de librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Configurar la conexión con el Backend (Opcional)
Si tienes el backend corriendo en otra dirección, edita el archivo `static/js/config.js` y ajusta la variable `API_BASE_URL`.

### 5. Ejecutar la aplicación
Arranca el servidor de desarrollo:
```bash
python app.py
```

### 6. Acceder a la web
Abre tu navegador y entra en: **[http://localhost:8080](http://localhost:8080)**

## Configuración importante

- `static/js/config.js`:
	- `API_BASE_URL`: URL base del backend separado. En desarrollo apunta a `http://127.0.0.1:8000`.
	- `USE_MOCK_API`: si `true`, `ApiService` usa un mock en memoria para pruebas sin backend; por defecto está en `false` para usar el backend real.

## Endpoints útiles

- Páginas:
	- `/` → `home` (plantilla `home.html`)
	- `/dashboard` → panel principal (`dashboard.html`)
	- `/login` → formulario de acceso (`login.html`)
	- `/seccion/<entity>` → vista genérica por entidad (`entity.html`)

- API esperada en el backend separado (`http://127.0.0.1:8000`):
	- `POST /api/auth/login` → autenticación y token
	- `GET/POST /api/<entity>` y `GET/PUT/DELETE /api/<entity>/<id>` → CRUD genérico para las entidades definidas en `app.py`

El servidor `app.py` solo sirve páginas y archivos estáticos. Los datos vienen siempre del backend separado.

## Credenciales

Las credenciales válidas las decide el backend real en `POST /api/auth/login`.

## Uso básico del frontend

1. Arrancar el backend real en `http://127.0.0.1:8000`.
2. Abrir `/login`, iniciar sesión con credenciales del backend.
3. Navegar al `/dashboard` o a `/seccion/<entity>` para listar y gestionar entidades.
4. Para cambiar a un backend externo, actualizar `static/js/config.js` con la URL del API y poner `USE_MOCK_API = false`.

## Pruebas (Tests)

Este proyecto incluye una suite de pruebas automatizadas con `pytest` que verifican la integridad de las rutas, la estructura de la UI y la lógica del frontend.

Para ejecutar los tests:

1. Asegúrate de tener las dependencias instaladas:
```bash
pip install -r requirements.txt
```

2. Ejecuta todos los tests:
```bash
PYTHONPATH=. pytest tests/
```

La suite cubre:
- Conectividad de todas las rutas y carga de recursos estáticos.
- Integridad de tablas y formularios para todas las entidades del gimnasio.
- Lógica de protección de rutas y filtrado por roles.
- Generación dinámica de botones de "Rellenado Rápido".

## Notas y siguientes pasos sugeridos

- Extender `ApiService` con manejo de refresh tokens y control de errores más robusto.
- Integrar Playwright para pruebas E2E completas con interacción de navegador.
