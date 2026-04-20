# MYSGYM - Frontend Dashboard

![Versión](https://img.shields.io/badge/version-1.0.0-blue)
![Licencia](https://img.shields.io/badge/license-MIT-green)

**MYSGYM** es una interfaz premium diseñada para la gestión inteligente de centros de fitness y rutinas de entrenamiento. Este proyecto está construido con tecnologías web puras para garantizar el máximo rendimiento y compatibilidad.

## 🚀 Características Principales

- **Diseño Ultra-Moderno**: Estética Glassmorphism con fondos dinámicos y tipografía optimizada.
- **Conexión API Flexible**: Estructura modular preparada para integrarse con bases de datos externas.
- **Interfaz Responsiva**: Adaptable a dispositivos móviles, tablets y escritorio.
- **Skeleton Loading**: Mejora la experiencia de usuario durante la carga de datos asíncronos.

## 🛠️ Tecnologías Utilizadas

- **HTML5 Semántico**: Para una estructura clara y mejor SEO.
- **Vanilla CSS**: Sin dependencias externas, con variables CSS para fácil personalización.
- **JavaScript (ES6+)**: Lógica reactiva y manejo de servicios API.
- **Google Fonts**: Fuentes 'Outfit' y 'Plus Jakarta Sans'.

## 📁 Estructura del Proyecto

```text
MYSGYM_FRONT/
├── assets/          # Recursos multimedia (iconos, imágenes)
├── css/             # Estilos globales y componentes
│   └── styles.css
├── js/              # Lógica de la aplicación
│   ├── api.js       # Servicio de comunicación con DB externa
│   └── main.js      # Manipulación del DOM y eventos
├── index.html       # Punto de entrada principal
└── README.md        # Documentación
```

## ⚙️ Configuración de la Base de Datos

Para conectar tu propia base de datos:
1. Dirígete a `js/api.js`.
2. Actualiza la `baseUrl` con la URL de tu backend.
3. Descomenta las líneas de `fetch` en los métodos de la clase `ApiService`.

## 📦 Instalación

No requiere herramientas de compilación. Simplemente clona el repositorio y abre `index.html` en tu navegador.

```bash
git clone https://github.com/MYSGYMN/MYSGYM_FRONT.git
```

---
Desarrollado con ❤️ para la comunidad Fitness.
