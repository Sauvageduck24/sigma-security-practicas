const proyectos = [];
let proyectoSeleccionadoId = null;


function agregarProyecto() { //FORMULARIO para añadir PROYECTO jejejejej
    const lista = document.getElementById('listaProyectos');

    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.innerHTML = `
        <input type="text" id="nuevoProyectoNombre" class="form-control mb-2" placeholder="Nombre del proyecto" maxlength="50">
        <textarea id="nuevoProyectoDescripcion" class="form-control mb-2" placeholder="Descripción (opcional)" maxlength="200"></textarea>
        <button class="btn btn-success btn-sm me-2" onclick="guardarNuevoProyecto()">Guardar</button>
        <button class="btn btn-danger btn-sm" onclick="this.parentElement.remove()">Cancelar</button>
    `;

    lista.prepend(li); // Añadir arriba del todo
}

function guardarNuevoProyecto() { //PARA AGREGAR EL WPROYECTO
    const nombre = document.getElementById('nuevoProyectoNombre').value.trim();
    const descripcion = document.getElementById('nuevoProyectoDescripcion').value.trim();

    if (nombre === '') {
        alert('El nombre del proyecto es obligatorio');
        return;
    }

    fetch('/api/proyectos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        //body: JSON.stringify({ nombre, descripcion, })
        body: JSON.stringify({ 'nombre':nombre,"descripcion":descripcion , "creador_id":1 }) // Cambiado a un solo objeto
    })
    .then(async response => {
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error('Error al crear proyecto: ' + errorText);
        }
        // Comprobar si hay contenido
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return {}; // Retornar objeto vacío si no hay JSON
        }
    })
    .then(data => {
        //console.log('Proyecto creado:', data);
        alert('Proyecto creado correctamente.');
        cargarProyectos();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error inesperado creando el proyecto. Revisa consola.');
    });
}

function renderizarProyectos() { //MOSTRAR LISTA DE PROYECTOS y ELIMINARLOS
    const lista = document.getElementById('listaProyectos');
    lista.innerHTML = '';

    proyectos.forEach((proyecto, index) => {
        const item = document.createElement('li');
        item.className = 'list-group-item text-white d-flex justify-content-between align-items-center';
        item.style.backgroundColor = '#1A2B49';
        item.dataset.index = index;

        if (proyecto.id === proyectoSeleccionadoId) {
            item.classList.add('proyecto-activo');
        }

        // Texto del nombre del proyecto
        const nombreSpan = document.createElement('span');
        nombreSpan.textContent = proyecto.nombre;
        nombreSpan.style.cursor = 'pointer';
        nombreSpan.addEventListener('click', () => seleccionarProyecto(index));

        // Botón de eliminar
        const eliminarBtn = document.createElement('button');
        eliminarBtn.className = 'btn btn-danger btn-sm';
        eliminarBtn.textContent = 'X';
        eliminarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
        
            const proyectoId = proyecto.id;
        
            fetch(`/api/proyectos/${proyectoId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) throw new Error("No se pudo eliminar el proyecto.");
                return response.json();
            })
            .then(data => {
                //console.log("Proyecto eliminado en backend:", data);
                // Quitar el proyecto de la lista local
                proyectos.splice(index, 1);
                renderizarProyectos();
            })
            .catch(error => {
                console.error("Error al eliminar proyecto:", error);
                alert("Hubo un error al eliminar el proyecto.");
            });
        });

        item.appendChild(nombreSpan);
        item.appendChild(eliminarBtn);
        lista.appendChild(item);
    });
}

function cargarProyectos() { //CARGAR PROYECTOS Y RENDERIZARLOS DESDE BD
    fetch('/api/proyectos') // Llamada a tu API real
        .then(response => response.json())
        .then(data => {
            proyectos.length = 0; // 🧹 Limpiar el array actual
            const proyectosFiltrados = data.filter(proyecto => proyecto.creador_id === usuario_id); // Filtrar por creador_id
            proyectos.push(...proyectosFiltrados); // ✅ Rellenarlo con los proyectos cargados del servidor

            renderizarProyectos(); // ✅ Ahora sí dibujarlos bien en pantalla
        })
        .catch(error => {
            console.error('Error cargando proyectos:', error);
        });
}


function seleccionarProyecto(indexSeleccionado) { //SELECCIONAR PROYECTO Y CARGARLO
    proyectoSeleccionadoId = proyectos[indexSeleccionado].id;
    renderizarProyectos();
    //console.log('Proyecto seleccionado:', proyectoSeleccionadoId);
    cargarMensajesDelProyecto(proyectoSeleccionadoId);
}



function cargarMensajesDelProyecto(proyectoId) { //CARGAR MENSAJES PROYECTO POR ID BD
    fetch(`/api/proyectos/${proyectoId}/mensajes`)
        .then(response => response.json())
        .then(mensajes => {
            mensajes.unshift({ contenido: 'Hola, soy el bot. ¿En qué puedo ayudarte?', id: null }); // Añadir mensaje inicial del bot
            //console.log('Mensajes cargados:', mensajes);

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML = ''; // vacia el chjat

            mostrarMensajesEnPantalla(mensajes); // (debes tener esta función)
        })
        .catch(error => {
            console.error('Error cargando mensajes:', error);
        });
}

// function mostrarMensajesEnPantalla(mensajes) {
//     const chatBox = document.getElementById('chat-box');
    
//     mensajes.forEach(mensaje => {
//         const clase = mensaje.usuario_id ? 'mensaje_usuario' : 'mensaje_bot';
//         mostrarMensaje(mensaje.contenido, clase);
//     });

//     chatBox.scrollTop = chatBox.scrollHeight; // Baja el scroll al final
// }

function mostrarMensajesEnPantalla(mensajes) { //ÑAPA
    const chatBox = document.getElementById('chat-box');
    
    let esUsuario = false;  // Empieza con el mensaje del usuario

    mensajes.forEach(mensaje => {
        // Alterna entre usuario y bot, siempre comienza con el usuario
        const clase = esUsuario ? 'mensaje_persona' : 'mensaje_bot';

        // Mostrar el mensaje con la clase correspondiente
        mostrarMensaje(mensaje.contenido, clase);

        // Alterna entre usuario y bot para el siguiente mensaje
        esUsuario = !esUsuario;
    });

    // Baja el scroll al final
    chatBox.scrollTop = chatBox.scrollHeight;
}



function mostrarMensaje(mensaje, clase) {
    const chatBox = document.getElementById('chat-box');

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
    } else {
        mensajeDiv.appendChild(mensajeContenido);
        mensajeDiv.appendChild(icono);
    }
    
    chatBox.appendChild(mensajeDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo el chat
}




function eliminarProyecto(index) {
    if (proyectos[index].id === proyectoSeleccionadoId) {
        proyectoSeleccionadoId = null;
    }
    proyectos.splice(index, 1);
    renderizarProyectos();
}

document.addEventListener('DOMContentLoaded', cargarProyectos);
