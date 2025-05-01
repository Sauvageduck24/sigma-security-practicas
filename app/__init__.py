from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db, User, Proyecto  # Importando el ORM de SQLAlchemy
import requests  # Importar requests para consumir la API
from sqlalchemy import text
from flask_cors import CORS
from api.app import api_bp
from api.chat import chat_bp
# Inicialización de la base de datos
from app.database import init_db,Mensaje
import flask_praetorian
from types import SimpleNamespace
import os

# Crear guardián de seguridad
guard = flask_praetorian.Praetorian()

base_dir = os.getcwd()
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.secret_key = 'super_secret_key'  # Necesario para sesiones

# 👉 Esta línea es esencial para Praetorian
app.config['JWT_SECRET_KEY'] = 'súper_secreta_para_tokens'

CORS(app)  # Permitir CORS si el frontend lo necesita
app.register_blueprint(api_bp, url_prefix="/api")  # Montar API en /api
app.register_blueprint(chat_bp, url_prefix="/chat")  # Montar chat en /chat

init_db(app)

# 👉 Inicializar Flask-Praetorian correctamente
#guard.init_app(app, User)  # Usa tu modelo de usuario

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class UserLogin(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.nombre = user.nombre
        self.is_admin = (user.nombre == "admin")

@app.route("/api/login", methods=["POST"])
def login_jwt():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = guard.authenticate(username, password)
    token = guard.encode_jwt_token(user)
    return jsonify({"access_token": token})

@login_manager.user_loader
def load_user(user_id):
    usuarios_response = requests.get(url_for('api.usuarios', _external=True))
    if usuarios_response.status_code == 200:
        usuarios = usuarios_response.json()
        user = next((u for u in usuarios if u['id'] == int(user_id)), None)
        if user:
            user_obj=SimpleNamespace(**user)
            return UserLogin(user_obj)
    return None

@app.route("/crear_admin", methods=["GET", "POST"])
def crear_admin():
    usuarios_response = requests.get(url_for('api.usuarios', _external=True))
    if usuarios_response.status_code == 200:
        usuarios = usuarios_response.json()
        if any(u['nombre'] == "admin" for u in usuarios):
            flash("Ya existe un usuario administrador.", "info")
            return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        contrasenya_hash = generate_password_hash(contrasenya)
        admin_user = User(nombre=nombre, contrasenya=contrasenya_hash)

        response = requests.post(url_for('api.usuarios', _external=True), json={"nombre": nombre, "contrasenya": contrasenya_hash})
        if response.status_code != 201:
            flash("Error al crear el usuario administrador", "danger")

        flash("Usuario administrador creado exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("crear_admin.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("sesion_iniciada"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        user_response = requests.get(url_for('api.usuarios', _external=True))
        if user_response.status_code == 200:
            usuarios = user_response.json()
            user = next((u for u in usuarios if u['nombre'] == nombre), None)

            if user and check_password_hash(user['contrasenya'], contrasenya):
                user_obj=SimpleNamespace(**user)
                login_user(UserLogin(user_obj))
                flash("Has iniciado sesión correctamente", "success")
                return redirect(url_for("home"))
            else:
                flash("Credenciales incorrectas", "danger")
        else:
            print("Error al obtener usuarios:", user_response.status_code)

    return render_template("login.html")

@app.route("/sesion_iniciada")
@login_required
def sesion_iniciada():
    return render_template("sesion_iniciada.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "success")
    return redirect(url_for("home"))

@app.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Acceso denegado: Solo el administrador puede ver esta página.", "danger")
        return redirect(url_for("home"))

    usuarios_response = requests.get(url_for('api.usuarios', _external=True))
    proyectos_response = requests.get(url_for('api.proyectos', _external=True))

    if usuarios_response.status_code == 200 and proyectos_response.status_code == 200:
        usuarios = usuarios_response.json()
        proyectos = proyectos_response.json()
    else:
        flash("Error al obtener datos desde la API", "danger")
        usuarios = []
        proyectos = []

    return render_template("admin_dashboard.html", usuarios=usuarios, proyectos=proyectos)

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.nombre == "admin":
        return redirect(url_for("admin_dashboard"))

    proyectos_response = requests.get(url_for('api.proyectos', _external=True))
    if proyectos_response.status_code == 200:
        proyectos = [p for p in proyectos_response.json() if p["creador_id"] == current_user.id]
    else:
        flash("Error al obtener proyectos desde la API", "danger")
        proyectos = []

    return render_template("dashboard.html", proyectos=proyectos, usuario_actual=current_user)

@app.route("/perfil")
@login_required
def perfil_usuario():
    usuario_response = requests.get(url_for('api.usuarios', _external=True))
    if usuario_response.status_code == 200:
        usuarios = usuario_response.json()
        usuario = next((u for u in usuarios if u['id'] == current_user.id), None)
    else:
        flash("Error al obtener datos del usuario desde la API", "danger")
        return redirect(url_for("home"))
    
    return render_template("perfil.html", usuario=usuario)

@app.route("/admin/crear_usuario", methods=["GET", "POST"])
@login_required
def crear_usuario():
    if not current_user.is_admin:
        flash("Acceso denegado: Solo el administrador puede crear usuarios.", "danger")
        return redirect(url_for('home'))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        contrasenya_hash = generate_password_hash(contrasenya)
        new_user = User(nombre=nombre, contrasenya=contrasenya_hash)

        usuario_response = requests.post(url_for('api.usuarios', _external=True), json={"nombre": nombre, "contrasenya": contrasenya_hash})
        if usuario_response.status_code != 201:
            flash("Error al crear el usuario", "danger")

        flash("Usuario creado exitosamente", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("crear_usuario.html")

@app.route("/admin/crear_proyecto", methods=["GET", "POST"])
@login_required
def crear_proyecto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        #new_proyecto = Proyecto(nombre=nombre, descripcion=descripcion, creador_id=current_user.id)

        nuevo_proyecto= {'nombre':nombre, 'descripcion':descripcion, 'creador_id':current_user.id}
        response = requests.post(url_for('api.proyectos', _external=True), json=nuevo_proyecto)

        flash("Proyecto creado exitosamente", "success")
        return redirect(url_for('dashboard'))

    return render_template("crear_proyecto.html")

@app.route("/api/proyectos", methods=["POST"]) #CREAR PROYECTO
@login_required
def crear_proyecto_api():
    data = request.get_json()

    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    new_proyecto = Proyecto(nombre=nombre, descripcion=descripcion, creador_id=current_user.id)

    try:
        response = requests.post(url_for('api.proyectos', _external=True), json=data)
        print("Proyecto creado con ID:", new_proyecto.id)

        return jsonify({
            "id": new_proyecto.id,
            "nombre": new_proyecto.nombre,
            "descripcion": new_proyecto.descripcion,
            "fecha_creacion": new_proyecto.fecha_creacion.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/proyectos", methods=["GET"])
@login_required
def listar_proyectos_api():
    try:
        print("Current user:", current_user.id)  # 👈 Añade esto para ver qué pasa
        #proyectos = Proyecto.query.filter_by(creador_id=current_user.id).all()
        proyectos_response = requests.get(url_for('api.proyectos', _external=True))
        if proyectos_response.status_code == 200:
            proyectos = [p for p in proyectos_response.json() if p["creador_id"] == current_user.id]
            proyectos_data = [
                {
                    "id": proyecto.id,
                    "nombre": proyecto.nombre,
                    "descripcion": proyecto.descripcion,
                    "fecha_creacion": proyecto.fecha_creacion.isoformat()
                }
                for proyecto in proyectos
            ]
            return jsonify(proyectos_data)
    except Exception as e:
        print("Error en listar_proyectos_api:", e)  # 👈 Captura el error en la consola Flask
        return jsonify({"error": str(e)}), 500

@app.route("/api/proyectos/<int:proyecto_id>", methods=["DELETE"])
@login_required
def eliminar_proyecto_api(proyecto_id):
    try:
        proyecto = Proyecto.query.filter_by(id=proyecto_id, creador_id=current_user.id).first()
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado o no autorizado"}), 404
        
        response = requests.delete(url_for('api.proyectos', _external=True) + f'?id={proyecto_id}')
        if response.status_code != 200:
            return jsonify({"error": "Error al eliminar el proyecto"}), 500

        return jsonify({"mensaje": "Proyecto eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/proyectos/<int:proyecto_id>/mensajes", methods=["POST"])
@login_required
def crear_mensajes(proyecto_id):
    data = request.get_json()

    contenido = data.get('contenido', '')

    if not contenido:
        return jsonify({"error": "El contenido es obligatorio"}), 400

    new_mensaje = Mensaje(
        contenido=contenido,
        proyecto_id=proyecto_id,
        usuario_id=current_user.id  # Opcional: si quieres registrar quién envió el mensaje
    )

    try:
        response = requests.post(url_for('api.mensajes', _external=True), json={'mensaje': contenido, 'proyecto_id': proyecto_id, 'usuario_id': current_user.id,'proyecto_id': proyecto_id})
        if response.status_code != 201:
            print("Error al crear el mensaje:", response.json())
            return jsonify({"error": "Error al crear el mensaje"}), 500

        print("Mensaje creado con ID:", new_mensaje.id)

        return jsonify({
            "id": new_mensaje.id,
            "contenido": new_mensaje.contenido
        }), 201
    except Exception as e:
        db.session.rollback()
        print("Error creando mensaje:", e)
        return jsonify({"error": str(e)}), 500
        
@app.route("/api/proyectos/<int:proyecto_id>/mensajes", methods=["GET"])
@login_required
def obtener_mensajes(proyecto_id):
    try:
        mensajes = Mensaje.query.filter_by(proyecto_id=proyecto_id).order_by(Mensaje.id.asc()).all()

        mensajes_data = [
            {
                "id": mensaje.id,
                "contenido": mensaje.contenido
            }
            for mensaje in mensajes
        ]

        return jsonify(mensajes_data)
    except Exception as e:
        print("Error en obtener_mensajes:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/chat-bot")
@login_required
def chat_bot():
    proyectos_response = requests.get(url_for('api.proyectos', _external=True))
    if proyectos_response.status_code == 200:
        proyectos = [p for p in proyectos_response.json() if p["creador_id"] == current_user.id]
        return render_template("chatbot.html", proyectos=proyectos,usuario_id=current_user.id)
    else:
        flash("Error al obtener proyectos desde la API", "danger")
        return redirect(url_for("dashboard"))

@app.route("/select-project")
def select_project():
    return render_template("select_project.html")

@app.route("/suma/<int:num1>/<int:num2>")
def suma(num1, num2):
    return render_template("suma.html", num1=num1, num2=num2, suma=num1 + num2)

@app.route("/test-db")
def test_db():
    try:
        result = db.session.execute(text("SELECT 1")).fetchone()
        return f"Conexión exitosa: {result}"
    except Exception as e:
        return f"Error conectando a la base de datos: {e}"

if __name__ == "__main__":
    app.run(debug=True)
