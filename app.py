from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
