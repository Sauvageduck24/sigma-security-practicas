from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db, init_db, User,Proyecto
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Necesario para sesiones

app = Flask(__name__, template_folder='../templates',static_folder='../static')

init_db(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Clase adaptadora para Flask-Login (porque tu modelo no hereda de UserMixin)
class UserLogin(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.nombre = user.nombre
        self.is_admin = (user.nombre == "admin")

# Función que Flask-Login necesita
@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    if user:
        return UserLogin(user)
    return None

# Nueva función para verificar si la BD está vacía o no tiene un admin
@app.before_request
def check_for_admin_or_empty_db():
    session = db.session
    if request.endpoint != "crear_admin" and request.endpoint != "static":
        # Verifica si no hay usuarios o no hay un admin
        if session.query(User).count() == 0 or not session.query(User).filter_by(nombre="admin").first():
            flash("No hay usuarios en la base de datos. Por favor, crea un usuario administrador.", "warning")
            return redirect(url_for("crear_admin"))

@app.route("/crear_admin", methods=["GET", "POST"])
def crear_admin():
    session = db.session
    # Redirige si ya existe un admin
    if session.query(User).filter_by(nombre="admin").first():
        flash("Ya existe un usuario administrador.", "info")
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        # Crea el usuario administrador
        contrasenya_hash = generate_password_hash(contrasenya)
        admin_user = User(nombre=nombre, contrasenya=contrasenya_hash)

        session.add(admin_user)
        session.commit()

        flash("Usuario administrador creado exitosamente. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("crear_usuario.html")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contrasenya = request.form["contrasenya"]

        user = db.session.query(User).filter_by(nombre=nombre).first()
        if user and check_password_hash(user.contrasenya, contrasenya):
            login_user(UserLogin(user))
            flash("Has iniciado sesión correctamente", "success")
            return redirect(url_for("home"))
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template("login.html")

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

    session = db.session
    usuarios = session.query(User).all()
    proyectos = session.query(Proyecto).all()
    return render_template("admin_dashboard.html", usuarios=usuarios,proyectos=proyectos)

@app.route("/dashboard")
@login_required
def dashboard():
    session = db.session
    proyectos = session.query(Proyecto).filter_by(creador_id=current_user.id).all()
    usuario_actual = session.query(User).filter_by(id=current_user.id).first()
    return render_template("dashboard.html", proyectos=proyectos,usuario_actual=usuario_actual)

@app.route("/perfil")
@login_required
def perfil_usuario():
    session = db.session
    usuario = session.query(User).filter_by(id=current_user.id).first()
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

        db.session.add(new_user)
        db.session.commit()

        flash("Usuario creado exitosamente", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template("crear_usuario.html")

@app.route("/admin/crear_proyecto", methods=["GET", "POST"])
@login_required
def crear_proyecto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        new_proyecto = Proyecto(nombre=nombre, descripcion=descripcion, creador_id=current_user.id)

        db.session.add(new_proyecto)
        db.session.commit()

        flash("Proyecto creado exitosamente", "success")
        return redirect(url_for('dashboard'))

    return render_template("crear_proyecto.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/chat-bot")
def chat_bot():
    proyectos=db.session.query(Proyecto).all()
    return render_template("chatbot.html",proyectos=proyectos)

@app.route("/select-project")
def select_project():
    return render_template("select_project.html")

@app.route("/suma/<int:num1>/<int:num2>")
def suma(num1,num2):
    print(num1, num2,num1+num2)
    return render_template("suma.html",num1=num1,num2=num2,suma=num1+num2)

# Nueva ruta para probar la conexión con la base de datos
@app.route("/test-db")
def test_db():
    try:
        # Ejecutar una consulta simple para probar la conexión
        with app.app_context():
            result = db.session.execute(text("SELECT 1")).fetchone()  # Cambiar 'SELECT 1' a text('SELECT 1')
        return f"Conexión exitosa: {result}"
    except Exception as e:
        return f"Error conectando a la base de datos: {e}"

if __name__ == "__main__":
    app.run(debug=True)