document.addEventListener('DOMContentLoaded', function() {
    const enviarBtn = document.getElementById('enviarBtn');
    const mensajeInput = document.getElementById('mensajeInput');
    const chatBox = document.querySelector('.chat-box');
    const mensajes = [];

    // Mostrar mensaje de bienvenida
    mostrarMensaje('Hola! Soy un bot, ¿en qué puedo ayudarte?', 'mensaje_bot');

    function enviarMensaje() {
        const mensaje = mensajeInput.value;
        if (mensaje.trim() !== '') {
            mostrarMensaje(mensaje, 'mensaje_persona');
            mensajes.push({ tipo: 'persona', mensaje: mensaje });
            mensajeInput.value = ''; // Limpiar el campo de entrada después de enviar el mensaje
            // Enviar el último mensaje en formato JSON
            enviarUltimoMensajeJSON(mensaje);
        }
    }

    function mostrarMensaje(mensaje, clase) {
        const mensajeDiv = document.createElement('div');
        mensajeDiv.classList.add('d-flex', clase === 'mensaje_bot' ? 'align-items-start' : 'justify-content-end', 'mb-3');
        
        const icono = document.createElement('div');
        icono.classList.add('icono');
        icono.innerHTML = clase === 'mensaje_bot' ? '🤖' : '👤';
        
        const mensajeContenido = document.createElement('div');
        mensajeContenido.classList.add(clase);
        mensajeContenido.textContent = mensaje;
        
        if (clase === 'mensaje_bot') {
            mensajeDiv.appendChild(icono);
            mensajeDiv.appendChild(mensajeContenido);
            mensajes.push({ tipo: 'bot', mensaje: mensaje });
        } else {
            mensajeDiv.appendChild(mensajeContenido);
            mensajeDiv.appendChild(icono);
        }
        
        chatBox.appendChild(mensajeDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo el chat
    }

    // function enviarUltimoMensajeJSON(mensaje) {
    //     const xhr = new XMLHttpRequest();
    //     xhr.open('POST', 'https://albertosalguero.eu.pythonanywhere.com/send-message', true);
    //     xhr.setRequestHeader('Content-Type', 'application/json');

    //     const json = JSON.stringify({ message: mensaje });

    //     xhr.onreadystatechange = function() {
    //         if (xhr.readyState === XMLHttpRequest.DONE) {
    //             if (xhr.status === 200) {
    //                 const respuesta = JSON.parse(xhr.responseText);
    //                 mostrarMensaje(respuesta.message, 'mensaje_bot');
    //             } else {
    //                 console.error('Error en la solicitud:', xhr.statusText);
    //             }
    //         }
    //     };

    //     console.log(json);
    //     xhr.send(json);
    // }

    function enviarUltimoMensajeJSON(mensaje) {
        if (proyectoSeleccionadoId === null) {
            alert('Selecciona un proyecto primero');
            return;
        }
    
        fetch('/chat/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: mensaje })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta recibida:', data);
    
            mostrarMensaje(data.message, 'mensaje_bot');
    
            // 🔵 Guardar el mensaje de la persona
            guardarMensajeEnBD(proyectoSeleccionadoId, mensaje, 'persona');
    
            // 🔵 Guardar el mensaje del bot
            guardarMensajeEnBD(proyectoSeleccionadoId, data.message, 'bot');
        })
        .catch(error => {
            console.error('Error al enviar mensaje:', error);
        });
    }

    function guardarMensajeEnBD(proyectoId, contenido, tipo) {
        fetch(`/api/proyectos/${proyectoId}/mensajes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ contenido: contenido, tipo: tipo })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Mensaje guardado en BD:', data);
        })
        .catch(error => {
            console.error('Error al guardar mensaje en BD:', error);
        });
    }
    

    
    enviarBtn.addEventListener('click', enviarMensaje);

    mensajeInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && proyectoSeleccionadoId !== null) {
            enviarMensaje();
        } else  if (proyectoSeleccionadoId == null){
            alert('Selecciona un proyecto primero');
        }
    });
});