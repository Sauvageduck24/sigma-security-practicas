from flask import Flask, render_template
from app.database import db, init_db  # Importar la base de datos y la inicialización
from sqlalchemy import text

app = Flask(__name__, template_folder='../templates',static_folder='../static')

init_db(app)  # Inicializar la base de datos con la aplicación Flask

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/chat-bot")
def chat_bot():
    return render_template("chatbot.html")

@app.route("/select-project")
def select_project():
    return render_template("select_project.html")

@app.route("/suma/<int:num1>/<int:num2>")
def suma(num1, num2):
    print(num1, num2, num1 + num2)

    return render_template("suma.html", num1=num1, num2=num2, suma=num1 + num2)

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

if __name__=='__main__':
    app.run(debug=True)