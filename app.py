from flask import Flask, redirect, render_template, request, url_for, jsonify, make_response

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    # Añade cabeceras CORS útiles para desarrollo local y preflight
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


DATABASE = {
    "usuarios": [
        {
            "id_usuario": 1,
            "nombre": "Leire Gomez",
            "email": "leire@mysgym.es",
            "password": "demo123",
            "telefono": "612345678",
            "fecha_registro": "2026-03-04",
            "estado": "activa",
        },
        {
            "id_usuario": 2,
            "nombre": "Iker Ruiz",
            "email": "iker@mysgym.es",
            "password": "demo123",
            "telefono": "622334455",
            "fecha_registro": "2026-03-18",
            "estado": "pendiente",
        },
    ],
    "empleados": [
        {
            "id_empleado": 1,
            "nombre": "Ane Salazar",
            "email": "ane@mysgym.es",
            "password": "demo123",
            "rol": "Entrenadora",
            "fecha_contratacion": "2025-09-01",
        },
        {
            "id_empleado": 2,
            "nombre": "Jon Bengoetxea",
            "email": "jon@mysgym.es",
            "rol": "Recepcion",
            "fecha_contratacion": "2025-11-15",
        },
    ],
    "salas": [
        {"id_sala": 1, "nombre": "Sala Fuerza", "capacidad": "18"},
        {"id_sala": 2, "nombre": "Studio Bike", "capacidad": "14"},
    ],
    "horarios": [
        {"id_horario": 1, "dia_semana": "Lunes", "hora_inicio": "07:00", "hora_fin": "08:00"},
        {"id_horario": 2, "dia_semana": "Miercoles", "hora_inicio": "18:00", "hora_fin": "19:00"},
    ],
    "actividades": [
        {
            "id_actividad": 1,
            "nombre": "Cross Training",
            "descripcion": "Alta intensidad",
            "monitor_id": "1",
            "sala_id": "1",
            "horario_id": "1",
            "aforo_maximo": "20",
        }
    ],
    "reservas": [
        {
            "id_reserva": 1,
            "usuario_id": "1",
            "actividad_id": "1",
            "fecha_reserva": "2026-04-22 07:00",
            "estado": "confirmada",
        }
    ],
    "material": [
        {"id_material": 1, "nombre": "Bicicletas indoor", "estado": "operativo", "sala_id": "2"},
        {"id_material": 2, "nombre": "Kettlebells", "estado": "revision", "sala_id": "1"},
    ],
    "incidencias": [
        {
            "id_incidencia": 1,
            "descripcion": "Bicicleta averiada",
            "fecha": "2026-04-18",
            "empleado_id": "2",
            "material_id": "1",
            "estado": "abierta",
        }
    ],
    "pagos": [
        {
            "id_pago": 1,
            "usuario_id": "1",
            "fecha_pago": "2026-04-01",
            "monto": "39.90",
            "metodo": "tarjeta",
        }
    ],
}


SCHEMA = {
    "usuarios": {
        "title": "Usuarios",
        "accent": "Entidad principal",
        "description": "Datos base de usuarios: nombre, email, telefono, fecha de registro y estado.",
        "id_field": "id_usuario",
        "fields": ["nombre", "email", "password", "telefono", "fecha_registro", "estado"],
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
        "fields": ["usuario_id", "fecha_pago", "monto", "metodo"],
    },
}


def next_id(entity):
    id_field = SCHEMA[entity]["id_field"]
    rows = DATABASE[entity]
    if not rows:
        return 1
    return max(int(row[id_field]) for row in rows) + 1


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


def find_record(entity, record_id):
    if entity not in SCHEMA:
        return None

    id_field = SCHEMA[entity]["id_field"]
    for row in DATABASE[entity]:
        if int(row[id_field]) == record_id:
            return row
    return None


@app.context_processor
def inject_navigation():
    return {"nav_items": nav_items(), "status_class": status_class}


@app.route("/")
def home():
    # NOTA: la implementación original construía los datos del tablero a
    # partir de la base de datos en memoria `DATABASE`. Cuando el frontend
    # consuma una API backend separada, estas inyecciones de datos en el
    # servidor deben eliminarse y el cliente debe obtenerlos mediante
    # JavaScript (ApiService).
    # El código siguiente devuelve intencionadamente valores vacíos/por
    # defecto para que las plantillas se muestren mientras el código
    # cliente recupera los datos reales.
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


@app.route('/dashboard')
def dashboard():
    # Página del frontend que usa JS para listar entidades; el backend
    # solo devuelve la plantilla.
    return render_template('dashboard.html', active_page='dashboard')


@app.route('/login')
def login():
    return render_template('login.html', active_page='login')


@app.route("/seccion/<entity>")
def entity_page(entity):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    config = SCHEMA[entity]
    # When using an external API, the entity rows and edit target are
    # fetched client-side. Return only the `config` metadata here.
    return render_template(
        "entity.html",
        entity=entity,
        config=config,
        rows=[],
        editing_record=None,
        active_page=entity,
    )


@app.post("/add/<entity>")
def add_record(entity):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    config = SCHEMA[entity]
    record = {config["id_field"]: next_id(entity)}
    for field in config["fields"]:
        record[field] = request.form.get(field, "").strip()

    DATABASE[entity].append(record)
    return redirect(url_for("entity_page", entity=entity))


@app.post("/update/<entity>/<int:record_id>")
def update_record(entity, record_id):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    config = SCHEMA[entity]
    record = find_record(entity, record_id)
    if record is None:
        return redirect(url_for("entity_page", entity=entity))

    for field in config["fields"]:
        record[field] = request.form.get(field, "").strip()

    return redirect(url_for("entity_page", entity=entity))


@app.post("/delete/<entity>/<int:record_id>")
def delete_record(entity, record_id):
    if entity not in SCHEMA:
        return redirect(url_for("home"))

    id_field = SCHEMA[entity]["id_field"]
    DATABASE[entity] = [
        row for row in DATABASE[entity] if int(row[id_field]) != record_id
    ]
    return redirect(url_for("entity_page", entity=entity))


if __name__ == "__main__":
    app.run(port=8080, debug=True)


### --- Simple test API endpoints (dev only) ---------------------------------


@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip()
    password = (data.get('password') or '')

    # Short-circuit test credentials
    if email == 'admin' and password == 'admin':
        resp = jsonify({'access_token': 'demo-admin-token', 'role': 'admin'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    if email == 'empleado' and password == 'empleado':
        resp = jsonify({'access_token': 'demo-employee-token', 'role': 'empleado'})
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # Try to match a user in in-memory DATABASE
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

