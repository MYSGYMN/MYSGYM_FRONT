import os

from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")


SCHEMA = {
    "usuarios": {
        "title": "Usuarios",
        "accent": "Entidad principal",
        "description": "Datos base de usuarios: nombre, email, telefono, fecha de registro y estado.",
        "id_field": "id_usuario",
        "fields": ["nombre", "email", "password", "telefono", "fecha_registro", "estado"],
        "examples": [
            {"nombre": "Ana Garcia", "email": "ana@gym.com", "password": "123", "telefono": "600123456", "fecha_registro": "2026-01-10", "estado": "activo"},
            {"nombre": "Carlos Lopez", "email": "carlos@gym.com", "password": "123", "telefono": "600123457", "fecha_registro": "2026-02-15", "estado": "activo"},
            {"nombre": "Laura Martinez", "email": "laura@gym.com", "password": "123", "telefono": "600123458", "fecha_registro": "2026-03-20", "estado": "inactivo"},
            {"nombre": "David Fernandez", "email": "david@gym.com", "password": "123", "telefono": "600123459", "fecha_registro": "2026-04-05", "estado": "activo"},
            {"nombre": "Elena Gomez", "email": "elena@gym.com", "password": "123", "telefono": "600123450", "fecha_registro": "2026-04-28", "estado": "activo"},
        ]
    },
    "empleados": {
        "title": "Empleados",
        "accent": "Recursos humanos",
        "description": "Personal del gimnasio con rol, email y fecha de contratacion.",
        "id_field": "id_empleado",
        "fields": ["nombre", "email", "rol", "fecha_contratacion"],
        "examples": [
            {"nombre": "Monitor Yoga", "email": "yoga@gym.com", "rol": "monitor", "fecha_contratacion": "2025-01-01"},
            {"nombre": "Monitor Spinning", "email": "spinning@gym.com", "rol": "monitor", "fecha_contratacion": "2025-06-15"},
            {"nombre": "Monitor Boxeo", "email": "boxeo@gym.com", "rol": "monitor", "fecha_contratacion": "2025-09-10"},
            {"nombre": "Monitora Pilates", "email": "pilates@gym.com", "rol": "monitor", "fecha_contratacion": "2026-01-20"},
            {"nombre": "Monitor CrossFit", "email": "crossfit@gym.com", "rol": "monitor", "fecha_contratacion": "2026-03-01"},
        ]
    },
    "salas": {
        "title": "Salas",
        "accent": "Infraestructura",
        "description": "Espacios fisicos del gimnasio con nombre y capacidad.",
        "id_field": "id_sala",
        "fields": ["nombre", "capacidad"],
        "examples": [
            {"nombre": "Sala de Yoga", "capacidad": 10},
            {"nombre": "Zona Musculación", "capacidad": 8},
            {"nombre": "Boxeo Pro", "capacidad": 5},
            {"nombre": "Sala de Pilates", "capacidad": 12},
            {"nombre": "Zona CrossFit", "capacidad": 15},
        ]
    },
    "horarios": {
        "title": "Horarios",
        "accent": "Planificacion",
        "description": "Dias y tramos horarios usados por las actividades.",
        "id_field": "id_horario",
        "fields": ["dia_semana", "hora_inicio", "hora_fin"],
        "examples": [
            {"dia_semana": "Lunes", "hora_inicio": "09:00", "hora_fin": "10:00"},
            {"dia_semana": "Martes", "hora_inicio": "10:30", "hora_fin": "11:30"},
            {"dia_semana": "Miercoles", "hora_inicio": "18:30", "hora_fin": "19:30"},
            {"dia_semana": "Jueves", "hora_inicio": "19:00", "hora_fin": "20:00"},
            {"dia_semana": "Viernes", "hora_inicio": "12:00", "hora_fin": "13:00"},
        ]
    },
    "actividades": {
        "title": "Actividades",
        "accent": "Operacion",
        "description": "Actividad ligada a un monitor, una sala, un horario y un aforo maximo.",
        "id_field": "id_actividad",
        "fields": ["nombre", "descripcion", "monitor", "sala", "horario", "aforo_maximo"],
        "form_fields": ["nombre", "descripcion", "monitor_id", "sala_id", "horario_id", "aforo_maximo"],
        "examples": [
            {"nombre": "Yoga Flow", "descripcion": "Clase relajante para empezar el día", "monitor_id": 1, "sala_id": 1, "horario_id": 1, "aforo_maximo": 10},
            {"nombre": "Spinning Extremo", "descripcion": "Alta intensidad sobre la bici", "monitor_id": 2, "sala_id": 2, "horario_id": 2, "aforo_maximo": 8},
            {"nombre": "Boxeo Táctico", "descripcion": "Técnica y resistencia en el ring", "monitor_id": 3, "sala_id": 3, "horario_id": 3, "aforo_maximo": 5},
            {"nombre": "Pilates Core", "descripcion": "Fortalecimiento del abdomen", "monitor_id": 4, "sala_id": 4, "horario_id": 4, "aforo_maximo": 12},
            {"nombre": "WOD CrossFit", "descripcion": "Entrenamiento del día exigente", "monitor_id": 5, "sala_id": 5, "horario_id": 5, "aforo_maximo": 15},
        ]
    },
    "reservas": {
        "title": "Reservas",
        "accent": "Relacion",
        "description": "Reserva de un usuario para una actividad en una fecha concreta.",
        "id_field": "id_reserva",
        "fields": ["usuario", "actividad", "sala", "horario", "fecha_reserva", "estado"],
        "form_fields": ["usuario_id", "actividad_id", "fecha_reserva", "estado"],
        "examples": [
            {"usuario_id": 1, "actividad_id": 1, "fecha_reserva": "2026-05-01T09:00:00", "estado": "confirmada"},
            {"usuario_id": 2, "actividad_id": 2, "fecha_reserva": "2026-05-02T10:30:00", "estado": "confirmada"},
            {"usuario_id": 3, "actividad_id": 3, "fecha_reserva": "2026-05-03T18:30:00", "estado": "pendiente"},
            {"usuario_id": 4, "actividad_id": 4, "fecha_reserva": "2026-05-04T19:00:00", "estado": "confirmada"},
            {"usuario_id": 5, "actividad_id": 5, "fecha_reserva": "2026-05-05T12:00:00", "estado": "cancelada"},
        ]
    },
    "material": {
        "title": "Material",
        "accent": "Inventario",
        "description": "Material del gimnasio con estado y sala asociada.",
        "id_field": "id_material",
        "fields": ["nombre", "estado", "sala"],
        "form_fields": ["nombre", "estado", "sala_id"],
        "examples": [
            {"nombre": "Mancuernas 5kg", "estado": "bueno", "sala_id": 1},
            {"nombre": "Bicicleta Estatica", "estado": "bueno", "sala_id": 2},
            {"nombre": "Saco de Boxeo", "estado": "desgastado", "sala_id": 3},
            {"nombre": "Esterilla Pilates", "estado": "nuevo", "sala_id": 4},
            {"nombre": "Kettlebell 16kg", "estado": "bueno", "sala_id": 5},
        ]
    },
    "incidencias": {
        "title": "Incidencias",
        "accent": "Mantenimiento",
        "description": "Incidencias sobre material registradas por empleados.",
        "id_field": "id_incidencia",
        "fields": ["descripcion", "fecha", "empleado", "material", "estado"],
        "form_fields": ["descripcion", "fecha", "empleado_id", "material_id", "estado"],
        "examples": [
            {"descripcion": "Falta limpieza general", "fecha": "2026-04-29", "empleado_id": 1, "material_id": 1, "estado": "pendiente"},
            {"descripcion": "Pedal derecho atascado", "fecha": "2026-04-30", "empleado_id": 2, "material_id": 2, "estado": "revision"},
            {"descripcion": "Costura del saco rota", "fecha": "2026-05-01", "empleado_id": 3, "material_id": 3, "estado": "abierta"},
            {"descripcion": "Esterilla manchada", "fecha": "2026-05-02", "empleado_id": 4, "material_id": 4, "estado": "resuelta"},
            {"descripcion": "Pesa oxidada en el mango", "fecha": "2026-05-03", "empleado_id": 5, "material_id": 5, "estado": "pendiente"},
        ]
    },
    "pagos": {
        "title": "Pagos",
        "accent": "Facturacion",
        "description": "Pagos hechos por usuarios con fecha, importe y metodo.",
        "id_field": "id_pago",
        "fields": ["usuario", "fecha_pago", "monto", "metodo"],
        "form_fields": ["usuario_id", "fecha_pago", "monto", "metodo"],
        "examples": [
            {"usuario_id": 1, "fecha_pago": "2026-04-29", "monto": 45.0, "metodo": "Tarjeta"},
            {"usuario_id": 2, "fecha_pago": "2026-04-30", "monto": 45.0, "metodo": "Efectivo"},
            {"usuario_id": 3, "fecha_pago": "2026-05-01", "monto": 50.0, "metodo": "Transferencia"},
            {"usuario_id": 4, "fecha_pago": "2026-05-02", "monto": 40.0, "metodo": "Tarjeta"},
            {"usuario_id": 5, "fecha_pago": "2026-05-03", "monto": 45.0, "metodo": "Domiciliacion"},
        ]
    },
}


def nav_items():
    return [
        {
            "key": entity,
            "title": config["title"],
            "url": url_for("entity_page", entity=entity),
        }
        for entity, config in SCHEMA.items()
    ]


def sections():
    return [
        {
            "key": entity,
            "title": config["title"],
            "accent": config["accent"],
            "description": config["description"],
            "id_field": config["id_field"],
            "fields": config["fields"],
            "url": url_for("entity_page", entity=entity),
        }
        for entity, config in SCHEMA.items()
    ]


@app.context_processor
def inject_navigation():
    return {"nav_items": nav_items()}


@app.route("/")
def home():
    return render_template(
        "home.html",
        sections=sections(),
        schema=SCHEMA,
        active_page="home",
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


@app.route("/login")
def login():
    return render_template("login.html", active_page="login")


@app.route("/seccion/<entity>")
def entity_page(entity):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    return render_template(
        "entity.html",
        entity=entity,
        config=SCHEMA[entity],
        active_page=entity,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
