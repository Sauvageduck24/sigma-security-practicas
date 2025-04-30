from flask import Blueprint, request, jsonify
import requests
from flask_praetorian import auth_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/send-message", methods=["POST"])
def responder():
    data = request.get_json()
    mensaje_usuario = data.get("message", "")

    # Reenviar el mensaje al backend original
    try:
        response = requests.post(
            "https://albertosalguero.eu.pythonanywhere.com/send-message",
            json={"message": mensaje_usuario},
            timeout=5
        )
        response.raise_for_status()
        respuesta_data = response.json()
        return jsonify(respuesta_data)
    except requests.RequestException as e:
        print("Error al contactar con el backend externo:", e)
        return jsonify({"message": "Lo siento, hubo un error al procesar tu mensaje."}), 500
