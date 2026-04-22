# MYSGYM — Frontend (Flask + Jinja)

Este repositorio contiene el frontend de MYSGYM. Es una aplicación Flask que sirve plantillas Jinja y recursos estáticos. Los datos se obtienen desde un backend REST separado (no incluido aquí). Este README describe lo que hay implementado y cómo dejar el backend listo para conectar con el frontend.

Última actualización: 21 de abril de 2026

## Qué hay implementado (estado actual)

- El frontend sirve páginas con Flask (`app.py`) y plantillas en `templates/`.
- Servicio JavaScript para consumir la API: `static/js/api.js` (soporte JWT, manejo de errores, `login()`/`logout()`).
- Archivo de configuración: `static/js/config.js` — define `API_BASE_URL` (por defecto `http://localhost:5000`).
- Plantillas preparadas para carga cliente-side: `templates/home.html` y `templates/entity.html` contienen marcadores/placeholder; el cliente debe rellenarlos llamando a la API.
- Documento de integración: `docs/integration.md` con instrucciones detalladas y ejemplo de backend.

# MYSGYM — Frontend (Flask + Jinja)

Este repositorio contiene el frontend de MYSGYM: una aplicación Flask que sirve plantillas Jinja y recursos estáticos. El repositorio está centrado en la interfaz y la experiencia cliente; no incluye un backend de datos completo.

Última actualización: 21 de abril de 2026

## Qué incluye este frontend

- `app.py`: servidor Flask que sirve plantillas y recursos estáticos.
- Plantillas Jinja en `templates/`: `base.html`, `home.html`, `entity.html`.
- Estilos en `static/css/styles.css`.
- Lógica cliente en `static/js/`:
	- `config.js`: define `API_BASE_URL` (valor por defecto `http://localhost:5000`).
	- `api.js`: `ApiService` preparado para trabajar con JWT (almacena token en `localStorage`, añade `Authorization` en peticiones, maneja errores).
	- `main.js`: comportamientos UI básicos (navegación, toasts, recarga).
- `docs/integration.md`: documento con contexto e instrucciones avanzadas (opcional).

## Estructura del proyecto

```
MYSGYM_FRONT/
├── app.py
├── templates/
├── static/
│   ├── css/styles.css
│   └── js/
│       ├── config.js
│       ├── api.js
│       └── main.js
├── docs/
└── README.md
```

## Cómo ejecutar el frontend localmente

1. Crear y activar un entorno virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar la dependencia necesaria:

```bash
pip install flask
```

3. Ejecutar la aplicación (por defecto sirve en el puerto 8080):

```bash
python app.py
# o: FLASK_APP=app.py flask run --port 8080
```

4. Abrir en el navegador: `http://localhost:8080`

## Notas sobre datos y API

- Las plantillas `home.html` y `entity.html` están preparadas para que los datos sean cargados por el cliente mediante llamadas a una API REST. Actualmente el servidor frontend devuelve placeholders para evitar errores si no hay API disponible.
- `static/js/config.js` contiene la variable `API_BASE_URL` para que el cliente sepa a qué backend llamar.

## Siguientes pasos posibles (opcional)

- Implementar `static/js/home.js` y `static/js/entity.js` para poblar la UI desde `ApiService`.
- Añadir una página de login y el flujo de autenticación usando `ApiService.login()`.

Si quieres que implemente cualquiera de estos pasos, dímelo y lo desarrollo.

---
Front-end preparado y organizado para integracion.

