import pytest
from app.database import db, User, Proyecto, Mensaje

# --- USUARIOS ---
def test_crear_usuario(client):
    response = client.post('/api/usuarios', json={
        'nombre': 'testuser',
        'contrasenya': 'testpass'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Usuario creado'


def test_obtener_usuarios(client):
    # Crear usuario primero
    client.post('/api/usuarios', json={'nombre': 'user2', 'contrasenya': 'pass2'})
    response = client.get('/api/usuarios')
    assert response.status_code == 200
    usuarios = response.get_json()
    assert any(u['nombre'] == 'user2' for u in usuarios)

# --- PROYECTOS ---
def test_crear_proyecto(client):
    # Crear usuario para asociar
    client.post('/api/usuarios', json={'nombre': 'projuser', 'contrasenya': 'pass'})
    usuarios = client.get('/api/usuarios').get_json()
    user_id = next(u['id'] for u in usuarios if u['nombre'] == 'projuser')
    response = client.post('/api/proyectos', json={
        'nombre': 'ProyectoTest',
        'descripcion': 'Desc',
        'creador_id': user_id
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Proyecto creado'


def test_obtener_proyectos(client):
    response = client.get('/api/proyectos')
    assert response.status_code == 200
    proyectos = response.get_json()
    assert isinstance(proyectos, list)

# --- MENSAJES ---
def test_crear_mensaje(client):
    # Crear usuario y proyecto
    client.post('/api/usuarios', json={'nombre': 'msguser', 'contrasenya': 'pass'})
    usuarios = client.get('/api/usuarios').get_json()
    user_id = next(u['id'] for u in usuarios if u['nombre'] == 'msguser')
    client.post('/api/proyectos', json={'nombre': 'MsgProyecto', 'descripcion': '', 'creador_id': user_id})
    proyectos = client.get('/api/proyectos').get_json()
    proyecto_id = next(p['id'] for p in proyectos if p['nombre'] == 'MsgProyecto')
    response = client.post('/api/mensajes', json={
        'mensaje': 'Hola mundo',
        'usuario_id': user_id,
        'proyecto_id': proyecto_id
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Mensaje creado'