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
    # Cuando se use una API externa, las filas de la entidad y el objetivo de
    # edición se obtienen desde el cliente. Devolver solo la metadata `config`
    # aquí.
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


### --- Endpoints de prueba simples (solo desarrollo) -------------------------


@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip()
    password = (data.get('password') or '')

    # Credenciales de prueba rápidas
    if email == 'admin' and password == 'admin':
        resp = jsonify({'access_token': 'demo-admin-token', 'role': 'admin'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    if email == 'empleado' and password == 'empleado':
        resp = jsonify({'access_token': 'demo-employee-token', 'role': 'empleado'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # Intentar hacer coincidir un usuario en la base de datos en memoria
    for u in DATABASE.get('usuarios', []):
        if str(u.get('email')) == email and str(u.get('password')) == password:
            role = 'admin' if int(u.get('id_usuario', 0)) == 1 else 'empleado'
            token = f"demo-token-{u.get('id_usuario')}"
            resp = jsonify({'access_token': token, 'role': role, 'user': u})
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    resp = make_response(jsonify({'message': 'Invalid credentials'}), 401)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def _find_entity_row(entity, record_id):
    id_field = SCHEMA[entity]['id_field']
    for r in DATABASE.get(entity, []):
        if int(r[id_field]) == int(record_id):
            return r
    return None


@app.route('/api/usuarios', methods=['GET', 'POST'])
def api_usuarios():
    if request.method == 'GET':
        resp = jsonify(DATABASE.get('usuarios', []))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # POST -> create
    data = request.get_json() or {}
    id_field = SCHEMA['usuarios']['id_field']
    new_id = next_id('usuarios')
    record = {id_field: new_id}
    for f in SCHEMA['usuarios']['fields']:
        record[f] = data.get(f, '')
    DATABASE['usuarios'].append(record)
    resp = make_response(jsonify(record), 201)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/api/usuarios/<int:record_id>', methods=['GET', 'PUT', 'DELETE'])
def api_usuario(record_id):
    id_field = SCHEMA['usuarios']['id_field']
    row = _find_entity_row('usuarios', record_id)
    if request.method == 'GET':
        if row is None:
            resp = make_response(jsonify({'message': 'Not found'}), 404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        resp = jsonify(row)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    if row is None:
        resp = make_response(jsonify({'message': 'Not found'}), 404)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    if request.method == 'PUT':
        data = request.get_json() or {}
        for f in SCHEMA['usuarios']['fields']:
            if f in data:
                row[f] = data.get(f)
        resp = jsonify(row)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # DELETE
    DATABASE['usuarios'] = [r for r in DATABASE['usuarios'] if int(r[id_field]) != int(record_id)]
    resp = make_response('', 204)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

