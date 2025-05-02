from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db, User, Proyecto, Mensaje, init_db
from flask_cors import CORS
from api.app import api_bp, obtener_usuarios, crear_usuario, eliminar_usuario, obtener_proyectos, crear_proyecto, eliminar_proyecto, obtener_mensajes, crear_mensaje
from api.chat import chat_bp
import flask_praetorian
import os

# Crear guardián de seguridad
guard = flask_praetorian.Praetorian()

base_dir = os.getcwd()
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))

application = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

application.secret_key = 'super_secret_key'
application.config['JWT_SECRET_KEY'] = 'súper_secreta_para_tokens'

CORS(application)

application.register_blueprint(api_bp, url_prefix="/api")
application.register_blueprint(chat_bp, url_prefix="/chat")

init_db(application)
guard.init_app(application, User)

@application.route("/api/login", methods=["POST"])
def login_jwt():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = guard.authenticate(username, password)
    token = guard.encode_jwt_token(user)
    return jsonify({"access_token": token})

@application.route("/crear_admin", methods=["GET", "POST"])
def crear_admin():
    usuarios = obtener_usuarios()
    if any(u['nombre'] == "admin" for u in usuarios):
        flash("Ya existe un usuario administrador.", "info")
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        contrasenya_hash = guard.hash_password(contrasenya)
        crear_usuario(nombre, contrasenya_hash)

        flash("Usuario administrador creado exitosamente", "success")
        return redirect(url_for("home"))

    return render_template("crear_admin.html")

@application.route("/")
def home():
    return render_template("index.html")

@application.route("/sesion_iniciada")
def sesion_iniciada():
    token=request.cookies.get("access_token")
    if not token:
        flash("Debes iniciar sesión para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user=guard.extract_jwt_token(token)
    return render_template("sesion_iniciada.html", usuario=user)

@application.route("/dashboard")
def dashboard():
    token=request.cookies.get("access_token")
    if not token:
        flash("Debes iniciar sesión para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user=guard.extract_jwt_token(token)
    if user['rls'] == "admin":
        return redirect(url_for("admin_dashboard"))

    proyectos = [p for p in obtener_proyectos() if p["creador_id"] == user['id']]
    user=next((u for u in obtener_usuarios() if u['id'] == user['id']), None)
    return render_template("dashboard.html", proyectos=proyectos, usuario_actual=user)

@application.route("/admin")
def admin_dashboard():
    token = request.cookies.get("access_token")
    if not token:
        flash("Debes iniciar sesión como administrador para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user = guard.extract_jwt_token(token)
    if user['rls'] != "admin":
        flash("Acceso denegado", "danger")
        return redirect(url_for("home"))

    usuarios = obtener_usuarios()
    proyectos = obtener_proyectos()
    return render_template("admin_dashboard.html", usuarios=usuarios, proyectos=proyectos)

@application.route("/logout")
def logout():
    flash("Sesión cerrada correctamente.", "info")
    response = redirect(url_for("home"))
    response.delete_cookie("access_token")
    return response

@application.route("/perfil")
def perfil_usuario():
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        flash("Debes iniciar sesión para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    usuario = next((u for u in obtener_usuarios() if u['id'] == user_data['id']), None)
    return render_template("perfil.html", usuario=usuario)

@application.route("/admin/crear_usuario", methods=["GET", "POST"])
def crear_usuario_app():
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        flash("Debes iniciar sesión como administrador para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    if user_data['rls'] != "admin":
        flash("Solo el administrador puede crear usuarios", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]
        contrasenya_hash = guard.hash_password(contrasenya)
        crear_usuario(nombre, contrasenya_hash)
        flash("Usuario creado exitosamente", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("crear_usuario.html")

@application.route("/admin/crear_proyecto", methods=["GET", "POST"])
def crear_proyecto_app():
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        flash("Debes iniciar sesión como administrador para acceder a esta página", "danger")
        return redirect(url_for("login"))
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        crear_proyecto(nombre, descripcion, user_data['id'])
        flash("Proyecto creado exitosamente", "success")
        return redirect(url_for("dashboard"))

    return render_template("crear_proyecto.html")

@application.route("/api/proyectos", methods=["POST"])
def crear_proyecto_api():
    data = request.get_json()
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token

    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    try:
        response = crear_proyecto(nombre, descripcion, user_data['id'])
        return jsonify(response), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@application.route("/api/proyectos", methods=["GET"])
def listar_proyectos_api():
    try:
        token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
        if not token:
            return jsonify({"error": "Token no proporcionado"}), 401
        
        user_data = guard.extract_jwt_token(token)  # Decodifica el token
        proyectos = [p for p in obtener_proyectos() if p["creador_id"] == user_data['id']]
        return jsonify(proyectos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application.route("/api/proyectos/<int:proyecto_id>", methods=["DELETE"])
def eliminar_proyecto_api(proyecto_id):
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    try:
        proyecto = Proyecto.query.filter_by(id=proyecto_id, creador_id=user_data['id']).first()
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado o no autorizado"}), 404
        eliminar_proyecto(proyecto_id)
        return jsonify({"mensaje": "Proyecto eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@application.route("/api/proyectos/<int:proyecto_id>/mensajes", methods=["POST"])
def crear_mensajes_app(proyecto_id):
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    data = request.get_json()
    contenido = data.get('contenido', '')

    if not contenido:
        return jsonify({"error": "El contenido es obligatorio"}), 400

    try:
        crear_mensaje(contenido, user_data['id'], proyecto_id)
        return jsonify({"mensaje": "Mensaje creado correctamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@application.route("/api/proyectos/<int:proyecto_id>/mensajes", methods=["GET"])
def obtener_mensajes_api(proyecto_id):
    token = request.cookies.get("access_token")
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401
    
    try:
        mensajes = Mensaje.query.filter_by(proyecto_id=proyecto_id).order_by(Mensaje.id.asc()).all()
        mensajes_data = [
            {"id": m.id, "contenido": m.contenido} for m in mensajes
        ]
        return jsonify(mensajes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application.route("/signin")
def signin():
    return render_template("signin.html")

@application.route("/login", methods=["GET", "POST"])
def login():
    token = request.cookies.get("access_token")
    
    if token:
        return redirect(url_for("sesion_iniciada"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        usuarios = obtener_usuarios()
        user = next((u for u in usuarios if u['nombre'] == nombre), None)

        if user:
            user = User(nombre=user["nombre"], contrasenya=user["contrasenya"],id=user["id"])
            try:
                if guard.authenticate(user.nombre, contrasenya):
                    token = guard.encode_jwt_token(user)
                    flash("Inicio de sesión exitoso", "success")
                    response = redirect(url_for("home"))
                    response.set_cookie("access_token", token, httponly=True, samesite="Lax")
                    return response
            except Exception:
                flash("Credenciales incorrectas", "danger")

    return render_template("login.html")


@application.route("/chat-bot")
def chat_bot():
    token = request.cookies.get("access_token")  # Asegúrate de obtener el token de la cookie
    if not token:
        flash("Debes iniciar sesión para acceder al chatbot", "danger")
        return redirect(url_for("home"))
    
    user_data = guard.extract_jwt_token(token)  # Decodifica el token
    proyectos = [p for p in obtener_proyectos() if p["creador_id"] == user_data['id']]
    return render_template("chatbot.html", proyectos=proyectos, usuario_id=user_data['id'])

@application.route("/select-project")
def select_project():
    return render_template("select_project.html")

@application.route("/suma/<int:num1>/<int:num2>")
def suma(num1, num2):
    return render_template("suma.html", num1=num1, num2=num2, suma=num1 + num2)

@application.route("/test-db")
def test_db():
    try:
        result = db.session.execute("SELECT 1").fetchone()
        return f"Conexión exitosa: {result}"
    except Exception as e:
        return f"Error conectando a la base de datos: {e}"

if __name__ == "__main__":
    application.run(debug=True)