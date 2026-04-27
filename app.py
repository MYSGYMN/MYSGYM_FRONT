import os
import base64
import hashlib
import hmac
import json
import time
import uuid

from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response

app = Flask(__name__)
FRONTEND_API_BASE_URL = os.getenv("FRONTEND_API_BASE_URL", "http://localhost:8000").rstrip("/")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
DEMO_CLIENT_EMAIL = os.getenv("DEMO_CLIENT_EMAIL", "cliente@mysgym.com")
DEMO_CLIENT_PASSWORD = os.getenv("DEMO_CLIENT_PASSWORD", "cliente123")
DEMO_ADMIN_EMAIL = os.getenv("DEMO_ADMIN_EMAIL", "admin@mysgym.com")
DEMO_ADMIN_PASSWORD = os.getenv("DEMO_ADMIN_PASSWORD", "admin123")

SCHEMA = {
    "usuarios": {
        "title": "Usuarios",
        "accent": "Entidad principal",
        "description": "Datos base de usuarios: nombre, email, telefono, fecha de registro y estado.",
        "id_field": "id_usuario",
        "fields": ["nombre", "email", "telefono", "fecha_registro", "estado"],
    },
    "empleados": {
        "title": "Empleados",
        "accent": "Recursos humanos",
        "description": "Personal del gimnasio con rol, email y fecha de contratacion.",
        "id_field": "id_empleado",
        "fields": ["nombre", "email", "rol", "fecha_contratacion"],
    },
    "salas": {
        "title": "Salas",
        "accent": "Infraestructura",
        "description": "Espacios fisicos del gimnasio con nombre y capacidad.",
        "id_field": "id_sala",
        "fields": ["nombre", "capacidad"],
    },
    "horarios": {
        "title": "Horarios",
        "accent": "Planificacion",
        "description": "Dias y tramos horarios usados por las actividades.",
        "id_field": "id_horario",
        "fields": ["dia_semana", "hora_inicio", "hora_fin"],
    },
    "actividades": {
        "title": "Actividades",
        "accent": "Operacion",
        "description": "Actividad ligada a un monitor, una sala, un horario y un aforo maximo.",
        "id_field": "id_actividad",
        "fields": ["nombre", "descripcion", "monitor_id", "sala_id", "horario_id", "aforo_maximo"],
    },
    "reservas": {
        "title": "Reservas",
        "accent": "Relacion",
        "description": "Reserva de un usuario para una actividad en una fecha concreta.",
        "id_field": "id_reserva",
        "fields": ["usuario_id", "actividad_id", "fecha_reserva", "estado"],
    },
    "material": {
        "title": "Material",
        "accent": "Inventario",
        "description": "Material del gimnasio con estado y sala asociada.",
        "id_field": "id_material",
        "fields": ["nombre", "estado", "sala_id"],
    },
    "incidencias": {
        "title": "Incidencias",
        "accent": "Mantenimiento",
        "description": "Incidencias sobre material registradas por empleados.",
        "id_field": "id_incidencia",
        "fields": ["descripcion", "fecha", "empleado_id", "material_id", "estado"],
    },
    "pagos": {
        "title": "Pagos",
        "accent": "Facturacion",
        "description": "Pagos hechos por usuarios con fecha, importe y metodo.",
        "id_field": "id_pago",
        "fields": ["usuario_id", "fecha_pago", "monto", "metodo_pago", "estado"],
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


def status_class(value):
    normalized = str(value).strip().lower()
    mapping = {
        "activa": "activo",
        "activo": "activo",
        "confirmada": "activo",
        "operativo": "activo",
        "cobrado": "cobrado",
        "pendiente": "pendiente",
        "en espera": "pendiente",
        "en proceso": "pendiente",
        "revision": "pendiente",
        "abierta": "inactivo",
        "inactiva": "inactivo",
        "inactivo": "inactivo",
    }
    return mapping.get(normalized, "pendiente")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def build_demo_jwt(identity, role):
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "fresh": False,
        "iat": now,
        "jti": str(uuid.uuid4()),
        "type": "access",
        "sub": str(identity),
        "role": role,
        "nbf": now,
        "exp": now + 60 * 60 * 24,
    }
    signing_input = f"{_b64url(json.dumps(header, separators=(',', ':')).encode())}.{_b64url(json.dumps(payload, separators=(',', ':')).encode())}"
    signature = hmac.new(
        JWT_SECRET_KEY.encode("utf-8"),
        signing_input.encode("ascii"),
        hashlib.sha256,
    ).digest()
    return f"{signing_input}.{_b64url(signature)}"


def demo_login_response(path, body):
    email = (body.get("email") or "").strip()
    password = body.get("password") or ""
    if email == DEMO_ADMIN_EMAIL and password == DEMO_ADMIN_PASSWORD:
        return jsonify(access_token=build_demo_jwt(1, "admin")), 200
    if email == DEMO_CLIENT_EMAIL and password == DEMO_CLIENT_PASSWORD:
        return jsonify(access_token=build_demo_jwt(1, "cliente")), 200
    return None


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.context_processor
def inject_navigation():
    return {
        "nav_items": nav_items(),
        "status_class": status_class,
        "frontend_runtime_config": {
            "apiBaseUrl": FRONTEND_API_BASE_URL,
        },
    }


@app.route("/")
def home():
    return render_template(
        "home.html",
        sections=[],
        latest_payments=[],
        distribution=[],
        total_records=0,
        active_users=0,
        open_issues=0,
        total_revenue=0,
        linked_entities=0,
        active_page="home",
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


@app.route("/login")
def login():
    return render_template("login.html", active_page="login")


@app.route("/register")
def register():
    return render_template("register.html", active_page="register")


@app.route("/seccion/<entity>")
def entity_page(entity):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    config = SCHEMA[entity]
    return render_template(
        "entity.html",
        entity=entity,
        config=config,
        rows=[],
        editing_record=None,
        active_page=entity,
    )


if __name__ == "__main__":
    app.run(port=8080, debug=True)
