from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../templates',static_folder='../static')

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

if __name__=='__main__':
    app.run(debug=True)