document.addEventListener('DOMContentLoaded', function() {
    const enviarBtn = document.getElementById('enviarBtn');
    const mensajeInput = document.getElementById('mensajeInput');
    const chatBox = document.querySelector('.chat-box');

    function enviarMensaje() {
        const mensaje = mensajeInput.value;
        if (mensaje.trim() !== '') {
            mostrarMensaje(mensaje, 'mensaje_persona');
            mensajeInput.value = ''; // Limpiar el campo de entrada después de enviar el mensaje
            setTimeout(() => {
                mostrarMensaje('mensaje respuesta', 'mensaje_bot');
            }, 1); // Esperar medio segundo antes de mostrar la respuesta del bot
        }
    }

    function mostrarMensaje(mensaje, clase) {
        const mensajeDiv = document.createElement('div');
        mensajeDiv.classList.add('d-flex', clase === 'mensaje_bot' ? 'align-items-start' : 'justify-content-end', 'mb-3');
        const mensajeContenido = document.createElement('div');
        mensajeContenido.classList.add(clase);
        mensajeContenido.textContent = mensaje;
        mensajeDiv.appendChild(mensajeContenido);
        chatBox.appendChild(mensajeDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo el chat
    }

    enviarBtn.addEventListener('click', enviarMensaje);

    mensajeInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            enviarMensaje();
        }
    });
});