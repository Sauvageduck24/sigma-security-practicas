const proyectos = ['Proyecto 1', 'Proyecto 2', 'Proyecto 3'];
let proyectoSeleccionado = null;

function renderizarProyectos() {
    const lista = document.getElementById('listaProyectos');
    lista.innerHTML = '';

    proyectos.forEach((nombre, index) => {
        const item = document.createElement('li');
        item.className = 'list-group-item text-white d-flex justify-content-between align-items-center';
        item.style.backgroundColor = '#1A2B49';
        item.dataset.index = index;

        if (index === proyectoSeleccionado) {
            item.classList.add('proyecto-activo');
        }

        // Texto del nombre del proyecto
        const nombreSpan = document.createElement('span');
        nombreSpan.textContent = nombre;
        nombreSpan.style.cursor = 'pointer';
        nombreSpan.addEventListener('click', () => seleccionarProyecto(index));

        // Botón de eliminar
        const eliminarBtn = document.createElement('button');
        eliminarBtn.className = 'btn btn-danger btn-sm';
        eliminarBtn.textContent = 'X';
        eliminarBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Para que no dispare el evento de selección
            eliminarProyecto(index);
        });

        item.appendChild(nombreSpan);
        item.appendChild(eliminarBtn);
        lista.appendChild(item);
    });
}

function seleccionarProyecto(indexSeleccionado) {
    proyectoSeleccionado = indexSeleccionado;
    renderizarProyectos();
    console.log('Proyecto seleccionado:', proyectos[proyectoSeleccionado]);
}

function agregarProyecto() {
    const nuevoNombre = prompt("Introduce el nombre del nuevo proyecto:");
    if (nuevoNombre) {
        proyectos.push(nuevoNombre);
        renderizarProyectos();
    }
}

function eliminarProyecto(index) {
    proyectos.splice(index, 1);

    // Si eliminamos el que estaba seleccionado, reiniciar selección
    if (proyectoSeleccionado === index) {
        proyectoSeleccionado = null;
    } else if (proyectoSeleccionado > index) {
        proyectoSeleccionado -= 1;
    }

    renderizarProyectos();
}

document.addEventListener('DOMContentLoaded', renderizarProyectos);
